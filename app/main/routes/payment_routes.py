import hashlib
import random
import string
import uuid
from datetime import datetime

from app.lib.aws import send_email
from app.lib.content import load_content
from app.lib.db_handler import (
    add_dynamics_payment,
    add_gov_uk_dynamics_payment,
    add_service_record_request,
    delete_dynamics_payment,
    delete_service_record_request,
    get_dynamics_payment,
    get_gov_uk_dynamics_payment,
    get_payment_id_from_record_id,
    hash_check,
    transform_form_data_to_record,
)
from app.lib.decorators.state_machine_decorator import with_state_machine
from app.lib.gov_uk_pay import (
    FAILED_PAYMENT_STATUSES,
    SUCCESSFUL_PAYMENT_STATUSES,
    UNFINISHED_PAYMENT_STATUSES,
    create_payment,
    get_payment_data,
    get_payment_status,
    process_valid_payment,
    process_valid_request,
    validate_payment,
)
from app.lib.models import db
from app.lib.price_calculations import calculate_amount_based_on_form_data
from app.main import bp
from app.main.forms.proceed_to_pay import ProceedToPay
from flask import current_app, redirect, render_template, request, session, url_for


@bp.route("/send-to-gov-uk-pay/")
def send_to_gov_uk_pay():
    """Initiate payment process for service record request."""
    form_data = session.get("form_data")

    if not form_data:
        current_app.logger.warning("No form data in session")
        return redirect(url_for("main.start"))

    try:
        record_hash = _generate_record_hash(form_data)
        if existing_record := hash_check(record_hash):
            if redirect_response := _handle_existing_payment(existing_record):
                return redirect_response

        payment_url = _create_new_payment(form_data, record_hash)
        return redirect(payment_url)

    except ValueError as e:
        current_app.logger.error(f"Validation error in payment creation: {e}")
        return redirect(url_for("main.payment_link_creation_failed"))
    except Exception as e:
        current_app.logger.error(f"Unexpected error in payment creation: {e}")
        return redirect(url_for("main.payment_link_creation_failed"))


def _generate_record_hash(form_data: dict) -> str:
    """Generate hash for form data to detect duplicates."""
    transformed_data = transform_form_data_to_record(form_data)
    return hashlib.sha256(str(transformed_data).encode()).hexdigest()


def _handle_existing_payment(existing_record):
    """Handle redirection for existing payment records."""
    payment_id = existing_record.payment_id
    payment_data = get_payment_data(payment_id)

    if not payment_data:
        current_app.logger.warning(
            f"Could not retrieve payment data for existing record: {existing_record.id}"
        )
        delete_service_record_request(existing_record)
        return None

    payment_status = get_payment_status(payment_data)

    if payment_status in SUCCESSFUL_PAYMENT_STATUSES:
        return redirect(url_for("main.confirm_payment_received"))
    elif payment_status in UNFINISHED_PAYMENT_STATUSES:
        return redirect(
            f"https://card.payments.service.gov.uk/card_details/{payment_id}"
        )
    elif payment_status in FAILED_PAYMENT_STATUSES:
        current_app.logger.info(f"Cleaning up failed payment: {payment_id}")
        delete_service_record_request(existing_record)

    return None


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
            "main.handle_gov_uk_pay_request_response", id=unique_id, _external=True
        ),
    )

    if not response:
        raise ValueError("Failed to create payment with GOV.UK Pay")

    payment_url = response.get("_links", {}).get("next_url", {}).get("href")
    payment_id = response.get("payment_id")

    if not payment_url or not payment_id:
        raise ValueError("Invalid payment response from GOV.UK Pay")

    _store_payment_record(form_data, record_hash, unique_id, payment_id)

    return payment_url


def _store_payment_record(
    form_data: dict, record_hash: str, unique_id: str, payment_id: str
):
    """Store payment record in database with transaction safety."""
    transformed_data = transform_form_data_to_record(form_data)

    data = {
        **transformed_data,
        "record_hash": record_hash,
        "id": unique_id,
        "payment_id": payment_id,
        "created_at": datetime.now(),
    }

    record = add_service_record_request(data)

    if record is None:
        raise ValueError("Failed to store payment record in database")

    current_app.logger.info(
        f"Created payment record: {unique_id} with payment ID: {payment_id}"
    )


def _validate_payment_id(id: str | None) -> tuple[str, int] | None:
    """
    Validate payment ID parameter.
    
    Args:
        id: Payment ID from request.
        
    Returns:
        tuple: Error message and status code if invalid, None if valid.
    """
    if not id:
        current_app.logger.warning("Payment response handler called without ID")
        return "Payment ID is required", 400
    return None


def _extract_payment_details(payment_data: dict) -> tuple[str | None, str | None]:
    """
    Extract provider ID and payment date from GOV.UK Pay data.
    
    Args:
        payment_data: Payment data from GOV.UK Pay API.
        
    Returns:
        tuple: (provider_id, payment_date) extracted from payment data.
    """
    provider_id = payment_data.get("provider_id")
    payment_date = payment_data.get("settlement_summary", {}).get("captured_date")
    return provider_id, payment_date


@bp.route("/handle-gov-uk-pay-payment-response/")
def handle_gov_uk_pay_payment_response():
    """Handle return from GOV.UK Pay for Dynamics payment flow."""
    id = request.args.get("id")

    if error := _validate_payment_id(id):
        return error

    payment = get_gov_uk_dynamics_payment(id)
    if payment is None:
        current_app.logger.warning(f"Payment not found for ID: {id}")
        return "Payment not found", 404

    gov_uk_payment_id = payment.gov_uk_payment_id
    gov_uk_payment_data = get_payment_data(gov_uk_payment_id)

    if gov_uk_payment_data is None:
        current_app.logger.error(
            f"Could not retrieve payment data for GOV.UK payment ID: {gov_uk_payment_id}"
        )
        # TODO: Create proper error page with payment ID for user reference
        return "Unable to retrieve payment information", 500

    if validate_payment(gov_uk_payment_data):
        provider_id, payment_date = _extract_payment_details(gov_uk_payment_data)
        try:
            process_valid_payment(
                payment.id, provider_id=provider_id, payment_date=payment_date
            )
        except Exception as e:
            current_app.logger.error(
                f"Error processing valid payment of payment ID {gov_uk_payment_id}: {e}"
            )

        return redirect(url_for("main.confirm_payment_received"))

    return redirect(url_for("main.payment_incomplete"))


@bp.route("/handle-gov-uk-pay-request-response/")
def handle_gov_uk_pay_request_response():
    """Handle return from GOV.UK Pay for service record request flow."""
    id = request.args.get("id")

    if error := _validate_payment_id(id):
        return error

    gov_uk_payment_id = get_payment_id_from_record_id(id)

    if gov_uk_payment_id is None:
        current_app.logger.warning(f"No payment ID found for record ID: {id}")
        return "Payment record not found", 404

    gov_uk_payment_data = get_payment_data(gov_uk_payment_id)

    if gov_uk_payment_data is None:
        current_app.logger.error(
            f"Could not retrieve payment data for GOV.UK payment ID: {gov_uk_payment_id}"
        )
        # TODO: Create proper error page with payment ID for user reference
        return "Unable to retrieve payment information", 500

    if validate_payment(gov_uk_payment_data):
        try:
            process_valid_request(gov_uk_payment_id, gov_uk_payment_data)
        except Exception as e:
            current_app.logger.error(
                f"Error processing valid request of payment ID {gov_uk_payment_id}: {e}"
            )

        return redirect(url_for("main.confirm_payment_received"))

    return redirect(url_for("main.payment_incomplete"))


@bp.route("/payment-link-creation_failed/")
def payment_link_creation_failed():
    content = load_content()
    return render_template(
        "main/payment/payment-link-creation-failed.html", content=content
    )


@bp.route("/payment-incomplete/")
def payment_incomplete():
    content = load_content()
    return render_template("main/payment/payment-incomplete.html", content=content)


@bp.route("/confirm-payment-received/")
def confirm_payment_received():
    content = load_content()
    return render_template(
        "main/payment/confirm-payment-received.html", content=content
    )


@bp.route("/return-from-gov-uk-pay/")
@with_state_machine
def return_from_gov_uk_pay(state_machine):
    state_machine.continue_on_return_from_gov_uk_redirect()
    return redirect(url_for(state_machine.route_for_current_state))


def _validate_required_fields(data: dict, required: list[str]) -> tuple[dict, int] | None:
    """
    Validate that all required fields are present.
    
    Args:
        data: Request data dictionary.
        required: List of required field names.
        
    Returns:
        tuple: Error response and status code if validation fails, None otherwise.
    """
    if missing := [field for field in required if field not in data]:
        return {"error": f"Missing required fields: {', '.join(missing)}"}, 400
    return None


def _convert_amount_to_pence(amount: float, field_name: str) -> tuple[int, None] | tuple[None, tuple[dict, int]]:
    """
    Convert amount from pounds to pence and validate.
    
    Args:
        amount: Amount in pounds.
        field_name: Name of the field for error messages.
        
    Returns:
        tuple: (converted_amount, None) on success, or (None, error_response) on failure.
    """
    try:
        pence = int(amount * 100)
        if pence <= 0:
            return None, ({"error": f"{field_name} must be greater than zero"}, 400)
        return pence, None
    except (ValueError, TypeError):
        return None, ({"error": f"Invalid {field_name} format"}, 400)


def _build_payment_data(data: dict) -> dict:
    """
    Build sanitized payment data dictionary.
    
    Args:
        data: Raw request data with validated amounts.
        
    Returns:
        dict: Sanitized payment data for database.
    """
    return {
        "case_number": data["case_number"],
        "reference": data["reference"],
        "net_amount": data["net_amount"],
        "total_amount": data["net_amount"] + data.get("delivery_amount", 0),
        "payee_email": data["payee_email"],
        "first_name": data.get("first_name", ""),
        "last_name": data.get("last_name", ""),
        "delivery_amount": data.get("delivery_amount", 0),
        "details": data.get("details", ""),
    }


@bp.route("/create-payment/", methods=["POST"])
def create_payment_endpoint():
    """
    Create a payment record and send email notification to payee.
    
    Required fields:
        - case_number: Case identifier
        - reference: Payment reference
        - net_amount: Net amount in pounds
        - payee_email: Email address of payee
        
    Optional fields:
        - delivery_amount: Delivery cost in pounds
        - first_name: Payee first name
        - last_name: Payee last name
        - details: Payment details description
        
    Returns:
        JSON response with message or error, and appropriate HTTP status code.
    """
    data = request.json
    required = ["case_number", "reference", "net_amount", "payee_email"]

    if error := _validate_required_fields(data, required):
        return error

    # Convert net amount to pence
    net_amount, error = _convert_amount_to_pence(data["net_amount"], "Net amount")
    if error:
        return error
    data["net_amount"] = net_amount

    # Convert delivery amount to pence if present
    if "delivery_amount" in data:
        delivery_amount, error = _convert_amount_to_pence(data["delivery_amount"], "Delivery amount")
        if error:
            return error
        data["delivery_amount"] = delivery_amount

    payment_data = _build_payment_data(data)
    payment = add_dynamics_payment(payment_data)
    
    if payment is None:
        return {"error": "Failed to create payment"}, 500

    try:
        payment.status = "S"  # Mark as Sent
        send_email(
            to=payment_data["payee_email"],
            subject="Payment for Service Record Request",
            body=f"You have been requested to make a payment for a service record request. Please visit the following link to complete your payment: {url_for('main.make_payment', id=payment.id, _external=True)}",
        )
        db.session.commit()
    except Exception as e:
        current_app.logger.error(
            f"Error sending payment email: {e}, deleting payment record."
        )
        delete_dynamics_payment(payment)
        return {"error": "Failed to create payment"}, 500

    return {"message": f"Payment created and sent successfully: {payment.id}"}, 201


@bp.route("/payment/<id>/", methods=["GET", "POST"])
def make_payment(id):
    """
    Display payment information and handle proceed to pay action.
    
    Args:
        id: Payment identifier.
        
    Returns:
        Rendered template or redirect to payment gateway.
    """
    form = ProceedToPay()
    payment = get_dynamics_payment(id)
    content = load_content()

    if payment is None:
        return "Payment not found", 404

    if form.validate_on_submit():
        return redirect(url_for("main.gov_uk_pay_redirect", id=payment.id))

    return render_template(
        "main/payment/dynamics-payment.html",
        form=form,
        payment=payment,
        content=content,
    )


def _build_payment_description(payment) -> str:
    """
    Build payment description from payment details.
    
    Args:
        payment: DynamicsPayment instance.
        
    Returns:
        str: Formatted payment description.
    """
    description = payment.case_number
    if payment.details:
        description += f": {payment.details}"
    return description


@bp.route("/payment-redirect/<id>/", methods=["GET"])
def gov_uk_pay_redirect(id):
    """
    Create GOV.UK Pay payment and redirect user to payment gateway.
    
    Args:
        id: Payment identifier.
        
    Returns:
        Redirect to GOV.UK Pay or error page.
    """
    payment = get_dynamics_payment(id)

    if payment is None:
        return "Payment not found", 404

    payment_link_id = str(uuid.uuid4())

    response = create_payment(
        amount=payment.total_amount,
        description=_build_payment_description(payment),
        reference=payment.reference,
        email=payment.payee_email,
        return_url=f"{url_for('main.handle_gov_uk_pay_payment_response', _external=True)}?id={payment_link_id}",
    )

    if not response:
        return redirect(url_for("main.payment_link_creation_failed"))

    # Safely extract payment URL from nested structure
    links = response.get("_links", {})
    next_url = links.get("next_url", {}) if isinstance(links, dict) else {}
    gov_uk_payment_url = next_url.get("href", "") if isinstance(next_url, dict) else ""
    gov_uk_payment_id = response.get("payment_id", "")

    if not gov_uk_payment_url or not gov_uk_payment_id:
        return redirect(url_for("main.payment_link_creation_failed"))

    gov_uk_payment_data = {
        "id": payment_link_id,
        "dynamics_payment_id": payment.id,
        "gov_uk_payment_id": gov_uk_payment_id,
        "created_at": datetime.now(),
    }

    add_gov_uk_dynamics_payment(gov_uk_payment_data)

    return redirect(gov_uk_payment_url)
