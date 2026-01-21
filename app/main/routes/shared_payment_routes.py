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
    """Fetch payment record from database based on payment type.

    Args:
        payment_type (str): Type of payment, either 'dynamics' or 'service_record'
        id (str): Payment record ID

    Returns:
        GOVUKDynamicsPayment | ServiceRecordRequest | None: Payment record or None if not found
    """
    if payment_type == "dynamics":
        return get_gov_uk_dynamics_payment(id)
    elif payment_type == "service_record":
        return get_service_record_request(id)
    return None


def _get_gov_uk_payment_data(gov_uk_payment_id):
    """Retrieve payment data from GOV.UK Pay API.

    Creates a GOV.UK Pay API client and fetches payment details. Logs an error
    if the API call fails or returns no data.

    Args:
        gov_uk_payment_id (str): GOV.UK Pay payment identifier

    Returns:
        GOVUKPayAPIClient: Client instance with payment data (may have None data if API call failed)
    """
    client = GOVUKPayAPIClient()
    client.get_payment(gov_uk_payment_id)

    if client.data is None:
        current_app.logger.error(
            f"Could not retrieve payment data for GOV.UK payment ID: {gov_uk_payment_id}"
        )

    return client


def _process_dynamics_payment(payment, client, gov_uk_payment_id):
    """Process a successful dynamics payment.

    Extracts provider ID and payment date from GOV.UK Pay response data
    and updates the dynamics payment record. Logs errors if processing fails.

    Args:
        payment: Dynamics payment record from database
        client (GOVUKPayAPIClient): Client with GOV.UK Pay payment data
        gov_uk_payment_id (str): GOV.UK Pay payment identifier for error logging
    """
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
    """Process a successful service record payment.

    Updates the service record request with payment data from GOV.UK Pay.
    Logs errors if processing fails.

    Args:
        payment: Service record request from database
        client (GOVUKPayAPIClient): Client with GOV.UK Pay payment data
        gov_uk_payment_id (str): GOV.UK Pay payment identifier for error logging
    """
    try:
        process_valid_request(payment.id, client.data)
    except Exception as e:
        current_app.logger.error(
            f"Error processing valid request of payment ID {gov_uk_payment_id}: {e}"
        )


@bp.route("/handle-gov-uk-pay-response/<payment_type>/<id>/")
def handle_gov_uk_pay_response(payment_type, id):
    """Handle the response from GOV.UK Pay after a payment attempt.

    This route is called when users return from the GOV.UK Pay service.
    It validates the payment type and ID, fetches payment data from both
    the local database and GOV.UK Pay API, and processes successful payments.

    Args:
        payment_type (str): Type of payment ('dynamics' or 'service_record')
        id (str): Local payment record ID

    Returns:
        Response: Redirect to appropriate page based on payment status

    Raises:
        400: Invalid payment type or missing ID
        404: Payment record not found in database
        502: Unable to retrieve payment data from GOV.UK Pay API
    """
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
        return redirect(url_for("main.confirm_payment_received"))
    else:
        _process_service_record_payment(payment, client, payment.gov_uk_payment_id)
        return redirect(url_for("main.request_submitted", id=payment.id))


@bp.route("/confirm-payment-received/")
def confirm_payment_received():
    """Display payment confirmation page for dynamics payments.

    Returns:
        str: Rendered confirmation template
    """
    content = load_content()
    return render_template(
        "main/payment/confirm-payment-received.html", content=content
    )


@bp.route("/payment-incomplete/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(PaymentIncomplete)
def payment_incomplete(form, state_machine):
    """Display payment incomplete page when payment fails or is cancelled.

    Allows users to continue from a failed payment attempt using the state machine
    to determine the next appropriate step in the journey.

    Args:
        form (PaymentIncomplete): Form for continuing the journey
        state_machine (RoutingStateMachine): State machine for navigation

    Returns:
        Response: Rendered template or redirect based on form submission
    """
    if form.validate_on_submit():
        state_machine.continue_from_payment_incomplete_page()
        return redirect(url_for(state_machine.route_for_current_state))
    content = load_content()
    return render_template(
        "main/payment/payment-incomplete.html", content=content, form=form
    )


@bp.route("/payment-link-creation-failed/")
def payment_link_creation_failed():
    """Display error page when GOV.UK Pay payment link creation fails.

    Returns:
        str: Rendered error template
    """
    content = load_content()
    return render_template(
        "main/payment/payment-link-creation-failed.html", content=content
    )
