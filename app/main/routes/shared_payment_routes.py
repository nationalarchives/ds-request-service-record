from app.lib.content import load_content
from app.lib.db.db_handler import (
    get_gov_uk_dynamics_payment,
    get_service_record_request,
)
from app.lib.gov_uk_pay import (
    GOVUKPayAPIClient,
    process_valid_payment,
    process_valid_request,
)
from app.main import bp
from flask import current_app, redirect, render_template, url_for


def _fetch_payment_by_type(payment_type, id):
    """Fetch payment record from database based on payment type."""
    if payment_type == "dynamics":
        return get_gov_uk_dynamics_payment(id)
    elif payment_type == "service_record":
        return get_service_record_request(id)
    return None


def _get_gov_uk_payment_data(gov_uk_payment_id):
    """Retrieve payment data from GOV.UK Pay API."""
    client = GOVUKPayAPIClient()
    client.get_payment(gov_uk_payment_id)

    if client.data is None:
        current_app.logger.error(
            f"Could not retrieve payment data for GOV.UK payment ID: {gov_uk_payment_id}"
        )

    return client


def _process_dynamics_payment(payment, client, gov_uk_payment_id):
    """Process a successful dynamics payment."""
    provider_id = client.data.get("provider_id", None)
    payment_date = client.data.get("settlement_summary", {}).get("captured_date", None)

    try:
        process_valid_payment(
            id=payment.dynamics_payment_id,
            provider_id=provider_id,
            payment_date=payment_date,
        )
    except Exception as e:
        current_app.logger.error(
            f"Error processing valid payment of payment ID {gov_uk_payment_id}: {e}"
        )


def _process_service_record_payment(payment, client, gov_uk_payment_id):
    """Process a successful service record payment."""
    try:
        process_valid_request(payment.id, client.data)
    except Exception as e:
        current_app.logger.error(
            f"Error processing valid request of payment ID {gov_uk_payment_id}: {e}"
        )


@bp.route("/handle-gov-uk-pay-response/<payment_type>/<id>/")
def handle_gov_uk_pay_response(payment_type, id):
    if not id or payment_type not in ["dynamics", "service_record"]:
        return "Shouldn't be here"

    payment = _fetch_payment_by_type(payment_type, id)
    if payment is None:
        return "Shouldn't be here"

    client = _get_gov_uk_payment_data(payment.gov_uk_payment_id)
    if client.data is None:
        return "Some sort of error"  # TODO: We need to make a proper error page for this to show we couldn't connect to GOV.UK Pay API - maybe provide the GOV.UK Pay ID and to contact webmaster?

    if not client.is_payment_successful():
        return redirect(url_for("main.payment_incomplete"))

    if payment_type == "dynamics":
        _process_dynamics_payment(payment, client, payment.gov_uk_payment_id)
        return redirect(url_for("main.confirm_payment_received"))
    else:
        _process_service_record_payment(payment, client, payment.gov_uk_payment_id)
        return redirect(url_for("main.request_submitted"))


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


@bp.route("/payment-link-creation-failed/")
def payment_link_creation_failed():
    content = load_content()
    return render_template(
        "main/payment/payment-link-creation-failed.html", content=content
    )
