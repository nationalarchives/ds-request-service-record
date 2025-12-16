import hashlib
import random
import string
import uuid
from datetime import datetime

from app.lib.aws import send_email
from app.lib.content import load_content
from app.lib.db import (
    db,
    SENT_STATUS,
    PAID_STATUS,
    NEW_STATUS,
    add_dynamics_payment,
    add_gov_uk_dynamics_payment,
    add_service_record_request,
    delete_dynamics_payment,
    delete_service_record_request,
    get_dynamics_payment,
    get_gov_uk_dynamics_payment,
    get_payment_id_from_record_id,
    get_service_record_request,
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
from app.lib.price_calculations import calculate_amount_based_on_form_data
from app.main import bp
from app.main.forms.proceed_to_pay import ProceedToPay
from flask import current_app, redirect, render_template, request, session, url_for


# @bp.route("/send-to-gov-uk-pay/")
# def send_to_gov_uk_pay():
#     """Initiate payment process for service record request."""
#     form_data = session.get("form_data")

#     if not form_data:
#         current_app.logger.warning("No form data in session")
#         return redirect(url_for("main.start"))

#     try:
#         record_hash = _generate_record_hash(form_data)
#         if existing_record := hash_check(record_hash):
#             if redirect_response := _handle_existing_payment(existing_record):
#                 return redirect_response

#         payment_url = _create_new_payment(form_data, record_hash)
#         return redirect(payment_url)

#     except ValueError as e:
#         current_app.logger.error(f"Validation error in payment creation: {e}")
#         return redirect(url_for("main.payment_link_creation_failed"))
#     except Exception as e:
#         current_app.logger.error(f"Unexpected error in payment creation: {e}")
#         return redirect(url_for("main.payment_link_creation_failed"))


# def _generate_record_hash(form_data: dict) -> str:
#     """Generate hash for form data to detect duplicates."""
#     transformed_data = transform_form_data_to_record(form_data)
#     return hashlib.sha256(str(transformed_data).encode()).hexdigest()


# def _handle_existing_payment(existing_record):
#     """Handle redirection for existing payment records."""
#     payment_id = existing_record.payment_id
#     payment_data = get_payment_data(payment_id)

#     if not payment_data:
#         current_app.logger.warning(
#             f"Could not retrieve payment data for existing record: {existing_record.id}"
#         )
#         delete_service_record_request(existing_record)
#         return None

#     payment_status = get_payment_status(payment_data)

#     if payment_status in SUCCESSFUL_PAYMENT_STATUSES:
#         return redirect(url_for("main.confirm_payment_received"))
#     elif payment_status in UNFINISHED_PAYMENT_STATUSES:
#         return redirect(
#             f"https://card.payments.service.gov.uk/card_details/{payment_id}"
#         )
#     elif payment_status in FAILED_PAYMENT_STATUSES:
#         current_app.logger.info(f"Cleaning up failed payment: {payment_id}")
#         delete_service_record_request(existing_record)

#     return None


# def _generate_reference() -> str:
#     """
#     Generate a unique payment reference using Unix timestamp, random letter, and suffix.
#     Format: TNA<timestamp><letter><suffix>
#     Example: TNA1733756789X42
#     """
#     unix_timestamp = int(datetime.now().strftime("%Y%m%d"))
#     random_letter = random.choice(string.ascii_uppercase)
#     random_suffix = random.randint(10, 99)

#     return f"TNA{unix_timestamp}{random_letter}{random_suffix}"


# def _create_new_payment(form_data: dict, record_hash: str) -> str:
#     """Create new payment and return payment URL."""
#     content = load_content()
#     unique_id = str(uuid.uuid4())

#     amount = calculate_amount_based_on_form_data(form_data)
#     if amount <= 0:
#         raise ValueError("Calculated amount must be greater than zero")

#     reference = _generate_reference()

#     response = create_payment(
#         amount=amount,
#         description=content["app"]["title"],
#         reference=reference,
#         email=form_data.get("requester_email"),
#         return_url=url_for(
#             "main.handle_gov_uk_pay_request_response", id=unique_id, _external=True
#         ),
#     )

#     if not response:
#         raise ValueError("Failed to create payment with GOV.UK Pay")

#     payment_url = response.get("_links", {}).get("next_url", {}).get("href")
#     payment_id = response.get("payment_id")

#     if not payment_url or not payment_id:
#         raise ValueError("Invalid payment response from GOV.UK Pay")

#     _store_payment_record(form_data, record_hash, unique_id, payment_id)

#     return payment_url


# def _store_payment_record(
#     form_data: dict, record_hash: str, unique_id: str, payment_id: str
# ):
#     """Store payment record in database with transaction safety."""
#     transformed_data = transform_form_data_to_record(form_data)

#     data = {
#         **transformed_data,
#         "record_hash": record_hash,
#         "id": unique_id,
#         "payment_id": payment_id,
#         "created_at": datetime.now(),
#     }

#     record = add_service_record_request(data)

#     if record is None:
#         raise ValueError("Failed to store payment record in database")

#     current_app.logger.info(
#         f"Created payment record: {unique_id} with payment ID: {payment_id}"
#     )


# @bp.route("/handle-gov-uk-pay-payment-response/")
# def handle_gov_uk_pay_payment_response():
#     id = request.args.get("id")

#     if not id:
#         # User got here without ID - likely manually, do something... (redirect to form?)
#         return "Shouldn't be here"

#     payment = get_gov_uk_dynamics_payment(id)
#     if payment is None:
#         # User got here with an ID that doesn't exist in the DB - could be our fault, or could be malicious, do something
#         return "Shouldn't be here"

#     gov_uk_payment_id = payment.gov_uk_payment_id
#     gov_uk_payment_data = get_payment_data(gov_uk_payment_id)

#     if gov_uk_payment_data is None:
#         # Could not retrieve payment data from GOV.UK Pay - log and inform user
#         current_app.logger.error(
#             f"Could not retrieve payment data for GOV.UK payment ID: {gov_uk_payment_id}"
#         )
#         return "Some sort of error"  # TODO: We need to make a proper error page for this to show we couldn't connect to GOV.UK Pay API - maybe provide the GOV.UK Pay ID and to contact webmaster?

#     if validate_payment(gov_uk_payment_data):
#         provider_id = gov_uk_payment_data.get("provider_id", None)
#         payment_date = gov_uk_payment_data.get("settlement_summary", {}).get(
#             "captured_date", None
#         )
#         try:
#             process_valid_payment(
#                 payment.id, provider_id=provider_id, payment_date=payment_date
#             )
#         except Exception as e:
#             current_app.logger.error(
#                 f"Error processing valid payment of payment ID {gov_uk_payment_id}: {e}"
#             )

#         return redirect(url_for("main.confirm_payment_received"))

#     # Let the user know it failed, ask if they want to retry
#     return redirect(url_for("main.payment_incomplete"))


# @bp.route("/handle-gov-uk-pay-request-response/")
# def handle_gov_uk_pay_request_response():
#     id = request.args.get("id")

#     if not id:
#         # User got here without ID - likely manually, do something... (redirect to form?)
#         return "Shouldn't be here"

#     gov_uk_payment_id = get_payment_id_from_record_id(id)

#     if gov_uk_payment_id is None:
#         # User got here with an ID that doesn't exist in the DB - could be our fault, or could be malicious, do something
#         return "Shouldn't be here"

#     gov_uk_payment_data = get_payment_data(gov_uk_payment_id)

#     if gov_uk_payment_data is None:
#         # Could not retrieve payment data from GOV.UK Pay - log and inform user
#         current_app.logger.error(
#             f"Could not retrieve payment data for GOV.UK payment ID: {gov_uk_payment_id}"
#         )
#         return "Some sort of error"  # TODO: We need to make a proper error page for this to show we couldn't connect to GOV.UK Pay API - maybe provide the GOV.UK Pay ID and to contact webmaster?

#     if validate_payment(gov_uk_payment_data):
#         try:
#             process_valid_request(gov_uk_payment_id, gov_uk_payment_data)
#         except Exception as e:
#             current_app.logger.error(
#                 f"Error processing valid request of payment ID {gov_uk_payment_id}: {e}"
#             )

#         return redirect(url_for("main.confirm_payment_received"))

#     # Let the user know it failed, ask if they want to retry
#     return redirect(url_for("main.payment_incomplete"))


# @bp.route("/payment-link-creation_failed/")
# def payment_link_creation_failed():
#     content = load_content()
#     return render_template(
#         "main/payment/payment-link-creation-failed.html", content=content
#     )


# @bp.route("/payment-incomplete/")
# def payment_incomplete():
#     content = load_content()
#     return render_template("main/payment/payment-incomplete.html", content=content)


# @bp.route("/confirm-payment-received/")
# def confirm_payment_received():
#     content = load_content()
#     return render_template(
#         "main/payment/confirm-payment-received.html", content=content
#     )


# @bp.route("/return-from-gov-uk-pay/")
# @with_state_machine
# def return_from_gov_uk_pay(state_machine):
#     state_machine.continue_on_return_from_gov_uk_redirect()
#     return redirect(url_for(state_machine.route_for_current_state))


# @bp.route("/payment-redirect/<id>/", methods=["GET"])
# def gov_uk_pay_redirect(id):
#     payment = get_dynamics_payment(id)

#     if payment is None:
#         return "Payment not found"

#     id = str(uuid.uuid4())

#     response = create_payment(
#         amount=payment.total_amount,
#         description=f"{payment.case_number}{': ' + payment.details if payment.details else ''}",
#         reference=payment.reference,
#         email=payment.payee_email,
#         return_url=f"{url_for("main.handle_gov_uk_pay_payment_response", _external=True)}?id={id}",
#     )

#     if not response:
#         return redirect(url_for("main.payment_link_creation_failed"))

#     gov_uk_payment_url = response.get("_links", {}).get("next_url", "").get("href", "")
#     gov_uk_payment_id = response.get("payment_id", "")

#     if not gov_uk_payment_url or not gov_uk_payment_id:
#         return redirect(url_for("main.payment_link_creation_failed"))

#     data = {
#         "id": id,
#         "dynamics_payment_id": payment.id,
#         "gov_uk_payment_id": gov_uk_payment_id,
#         "created_at": datetime.now(),
#     }

#     add_gov_uk_dynamics_payment(data)

#     return redirect(gov_uk_payment_url)

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

    except Exception as e:
        current_app.logger.error(f"Unexpected error in payment creation: {e}")
        return redirect(url_for("main.payment_link_creation_failed"))

@bp.route("/confirm-payment-received/")
def confirm_payment_received():
    content = load_content()
    return render_template(
        "main/payment/confirm-payment-received.html", content=content
    )

@bp.route("/handle-gov-uk-pay-response/<payment_type>/<id>/")
def handle_gov_uk_pay_response(payment_type, id):
    if payment_type == "dynamics":
        payment = get_gov_uk_dynamics_payment(id)
    elif payment_type == "service_record":
        payment = get_service_record_request(id)
    else:
        return "Shouldn't be here"
    
    if payment is None:
        # User got here with an ID that doesn't exist in the DB - could be our fault, or could be malicious, do something
        return "Shouldn't be here"
    
    gov_uk_payment_id = payment.gov_uk_payment_id
    gov_uk_payment_data = get_payment_data(gov_uk_payment_id) # TODO: <- improve this function to use the JSONAPIClient

    if gov_uk_payment_data is None:
        # Could not retrieve payment data from GOV.UK Pay - log and inform user
        current_app.logger.error(
            f"Could not retrieve payment data for GOV.UK payment ID: {gov_uk_payment_id}"
        )
        return "Some sort of error"  # TODO: We need to make a proper error page for this to show we couldn't connect to GOV.UK Pay API - maybe provide the GOV.UK Pay ID and to contact webmaster?
    
    if validate_payment(gov_uk_payment_data): # TODO: <- improve this function to use the JSONAPIClient
        if payment_type == "dynamics":
            provider_id = gov_uk_payment_data.get("provider_id", None)
            payment_date = gov_uk_payment_data.get("settlement_summary", {}).get(
                "captured_date", None
            ) # TODO <- improve this function to use the JSONAPIClient?
            try:
                process_valid_payment(
                    id=payment.dynamics_payment_id, provider_id=provider_id, payment_date=payment_date
                )
            except Exception as e:
                current_app.logger.error(
                    f"Error processing valid payment of payment ID {gov_uk_payment_id}: {e}"
                )
        elif payment_type == "service_record":
            try:
                process_valid_request(payment.id, gov_uk_payment_data)
            except Exception as e:
                current_app.logger.error(
                    f"Error processing valid request of payment ID {gov_uk_payment_id}: {e}"
                )    
        return redirect(url_for("main.confirm_payment_received"))

    # Let the user know it failed, ask if they want to retry
    return redirect(url_for("main.payment_incomplete"))
    

@bp.route("/payment-redirect/<id>/", methods=["GET"])
def gov_uk_pay_redirect(id):
    payment = get_dynamics_payment(id)

    if payment is None:
        return "Payment not found"

    id = str(uuid.uuid4())

    response = create_payment(
        amount=payment.total_amount,
        description=f"{payment.case_number}{(': ' + payment.details) if payment.details else ''}",
        reference=payment.reference,
        email=payment.payee_email,
        return_url=f"{url_for('main.handle_gov_uk_pay_response', payment_type='dynamics', id=id, _external=True)}",
    )

    if not response:
        return redirect(url_for("main.payment_link_creation_failed"))

    gov_uk_payment_url = response.get("_links", {}).get("next_url", {}).get("href", "")
    gov_uk_payment_id = response.get("payment_id", "")

    if not gov_uk_payment_url or not gov_uk_payment_id:
        return redirect(url_for("main.payment_link_creation_failed"))

    data = {
        "id": id,
        "dynamics_payment_id": payment.id,
        "gov_uk_payment_id": gov_uk_payment_id,
        "created_at": datetime.now(),
    }

    add_gov_uk_dynamics_payment(data)

    return redirect(gov_uk_payment_url)

def _hash_form_data(form_data: dict) -> str:
    """Generate hash for form data to detect duplicates."""
    transformed_data = transform_form_data_to_record(form_data)
    return hashlib.sha256(str(transformed_data).encode()).hexdigest()
