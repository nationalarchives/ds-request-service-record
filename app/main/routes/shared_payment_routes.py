from app.lib.content import load_content
from app.lib.db.db_handler import (
    get_gov_uk_dynamics_payment,
    get_service_record_request,
)
from app.lib.decorators.state_machine_decorator import with_state_machine
from app.lib.decorators.with_form_prefilled_from_session import (
    with_form_prefilled_from_session,
)
from app.lib.gov_uk_pay import (
    GOVUKPayAPIClient,
    process_valid_payment,
    process_valid_request,
)
from app.main import bp
from app.main.forms.payment_incomplete import PaymentIncomplete
from flask import abort, current_app, redirect, render_template, url_for


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
        abort(400, description="Invalid payment type or ID")

    payment = _fetch_payment_by_type(payment_type, id)
    if payment is None:
        abort(404, description="Payment record not found")

    client = _get_gov_uk_payment_data(payment.gov_uk_payment_id)
    if client.data is None:
        abort(502, description="Unable to retrieve payment data ")

    if not client.is_payment_successful():
        return redirect(url_for("main.payment_incomplete"))

    if payment_type == "dynamics":
        _process_dynamics_payment(payment, client, payment.gov_uk_payment_id)
    else:
        _process_service_record_payment(payment, client, payment.gov_uk_payment_id)

    return redirect(url_for("main.confirm_payment_received"))


@bp.route("/confirm-payment-received/")
def confirm_payment_received():
    content = load_content()
    return render_template(
        "main/payment/confirm-payment-received.html", content=content
    )


@bp.route("/payment-incomplete/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(PaymentIncomplete)
def payment_incomplete(form, state_machine):
    if form.validate_on_submit():
        state_machine.continue_from_payment_incomplete_page()
        return redirect(url_for(state_machine.route_for_current_state))
    content = load_content()
    return render_template(
        "main/payment/payment-incomplete.html", content=content, form=form
    )


@bp.route("/payment-link-creation-failed/")
def payment_link_creation_failed():
    content = load_content()
    return render_template(
        "main/payment/payment-link-creation-failed.html", content=content
    )
