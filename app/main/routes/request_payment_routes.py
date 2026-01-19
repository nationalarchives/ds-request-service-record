import hashlib
import random
import string
import uuid
from datetime import datetime

from app.lib.content import load_content
from app.lib.db.db_handler import (
    add_service_record_request,
    delete_service_record_request,
    hash_check,
    transform_form_data_to_record,
)
from app.lib.db.models import ServiceRecordRequest
from app.lib.decorators.state_machine_decorator import with_state_machine
from app.lib.gov_uk_pay import (
    FAILED_PAYMENT_STATUSES,
    SUCCESSFUL_PAYMENT_STATUSES,
    UNFINISHED_PAYMENT_STATUSES,
    GOVUKPayAPIClient,
    create_payment,
)
from app.lib.price_calculations import calculate_amount_based_on_form_data
from app.main import bp
from flask import current_app, redirect, session, url_for


@bp.route("/return-from-gov-uk-pay/")
@with_state_machine
def return_from_gov_uk_pay(state_machine):
    state_machine.continue_on_return_from_gov_uk_redirect()
    return redirect(url_for(state_machine.route_for_current_state))


@bp.route("/send-to-gov-uk-pay/")
def send_to_gov_uk_pay():
    """Initiate payment process for service record request."""
    form_data = session.get("form_data")

    if not form_data:
        current_app.logger.warning("No form data in session")
        return redirect(url_for("main.start"))

    transformed_data = transform_form_data_to_record(form_data)

    try:
        return _create_new_payment_or_redirect(transformed_data)

    except Exception as e:
        current_app.logger.error(f"Unexpected error in payment creation: {e}")
        return redirect(url_for("main.payment_link_creation_failed"))


def _create_new_payment_or_redirect(form_data: dict):

    record_hash = _hash_form_data(form_data)
    if existing_record := hash_check(record_hash):
        if redirect_response := _handle_existing_payment(existing_record):
            return redirect_response

    payment_url = _create_new_payment(form_data, record_hash)
    return redirect(payment_url)


def _hash_form_data(form_data: dict) -> str:
    """Generate hash for form data to detect duplicates."""
    return hashlib.sha256(str(form_data).encode()).hexdigest()


def _create_new_payment(form_data: dict, record_hash: str) -> str:
    """Create new payment and return payment URL."""
    content = load_content()
    unique_id = str(uuid.uuid4())

    amount = calculate_amount_based_on_form_data(form_data)

    if amount <= 0:
        raise ValueError("Calculated amount must be greater than zero")

    reference = _generate_reference()

    response = create_payment(
        amount=amount,
        description=content["app"]["title"],
        reference=reference,
        email=form_data.get("requester_email"),
        return_url=url_for(
            "main.handle_gov_uk_pay_response",
            payment_type="service_record",
            id=unique_id,
            _external=True,
        ),
    )

    if not response:
        raise ValueError("Failed to create payment with GOV.UK Pay")

    payment_url = response.get("_links", {}).get("next_url", {}).get("href")
    payment_id = response.get("payment_id")

    if not payment_url or not payment_id:
        raise ValueError("Invalid payment response from GOV.UK Pay")

    record = _store_payment_record(form_data, record_hash, unique_id, payment_id)

    if not record:
        return url_for("main.payment_link_creation_failed")

    return payment_url


def _generate_reference() -> str:
    """
    Generate a unique payment reference using Unix timestamp, random letter, and suffix.
    Format: TNA<timestamp><letter><suffix>
    Example: TNA1733756789X42
    """
    unix_timestamp = int(datetime.now().strftime("%Y%m%d"))
    random_letter = random.choice(string.ascii_uppercase)
    random_suffix = random.randint(10, 99)

    return f"TNA{unix_timestamp}{random_letter}{random_suffix}"


def _store_payment_record(
    form_data: dict, record_hash: str, unique_id: str, payment_id: str
) -> ServiceRecordRequest | None:
    """Store payment record in database with transaction safety."""

    data = {
        **form_data,
        "record_hash": record_hash,
        "id": unique_id,
        "gov_uk_payment_id": payment_id,
        "created_at": datetime.now(),
    }

    record = add_service_record_request(data)

    if record is None:
        raise ValueError("Failed to store payment record in database")

    current_app.logger.info(
        f"Created payment record: {unique_id} with payment ID: {payment_id}"
    )

    return record


def _handle_existing_payment(existing_record):
    """Handle redirection for existing payment records."""
    payment_id = existing_record.gov_uk_payment_id
    client = GOVUKPayAPIClient()
    client.get_payment(payment_id)

    if not client.data:
        current_app.logger.warning(
            f"Could not retrieve payment data for existing record: {existing_record.id}"
        )
        delete_service_record_request(existing_record)
        return None

    payment_status = client.get_payment_status()

    if payment_status in SUCCESSFUL_PAYMENT_STATUSES:
        return redirect(url_for("main.request_submitted"))
    elif payment_status in UNFINISHED_PAYMENT_STATUSES:
        return redirect(
            f"https://card.payments.service.gov.uk/card_details/{payment_id}"
        )
    elif payment_status in FAILED_PAYMENT_STATUSES:
        current_app.logger.info(f"Cleaning up failed payment: {payment_id}")
        delete_service_record_request(existing_record)

    return None
