from app.lib.db import get_gov_uk_dynamics_payment, get_service_record_request
from app.lib.gov_uk_pay import get_payment_data, validate_payment, process_valid_payment, process_valid_request
from flask import current_app, redirect, url_for
from app.main import bp
from flask import render_template
from app.lib.content import load_content


@bp.route("/handle-gov-uk-pay-response/<payment_type>/<id>/")
def handle_gov_uk_pay_response(payment_type, id):
    if not id:
        return "Shouldn't be here"

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

@bp.route("/confirm-payment-received/")
def confirm_payment_received():
    content = load_content()
    return render_template(
        "main/payment/confirm-payment-received.html", content=content
    )

@bp.route("/payment-incomplete/")
def payment_incomplete():
    content = load_content()
    return render_template("main/payment/payment-incomplete.html", content=content)

@bp.route("/payment-link-creation_failed/")
def payment_link_creation_failed():
    content = load_content()
    return render_template(
        "main/payment/payment-link-creation-failed.html", content=content
    )