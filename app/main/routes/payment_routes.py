import uuid
from datetime import datetime

from app.lib.aws import send_email
from app.lib.content import load_content
from app.lib.db_handler import (
    add_dynamics_payment,
    add_gov_uk_dynamics_payment,
    add_service_record_request,
    get_dynamics_payment,
    get_gov_uk_dynamics_payment,
    get_payment_id_from_record_id,
)
from app.lib.decorators.state_machine_decorator import with_state_machine
from app.lib.gov_uk_pay import (
    create_payment,
    get_payment_data,
    process_valid_payment,
    process_valid_request,
    validate_payment,
)
from app.main import bp
from app.main.forms.proceed_to_pay import ProceedToPay
from flask import current_app, redirect, render_template, request, session, url_for


@bp.route("/send-to-gov-uk-pay/")
def send_to_gov_pay():
    content = load_content()
    form_data = session.get("form_data", {})
    requester_email = form_data.get("requester_email", None)

    id = str(uuid.uuid4())

    response = create_payment(
        amount=1000,
        description=content["app"]["title"],
        reference="ServiceRecordRequest",
        email=requester_email,
        return_url=f"{url_for("main.handle_gov_uk_pay_response", _external=True)}?id={id}&response_type=request",
    )

    if not response:
        return redirect(url_for("main.payment_link_creation_failed"))

    payment_url = response.get("_links", {}).get("next_url", "").get("href", "")
    payment_id = response.get("payment_id", "")

    if not payment_url or not payment_id:
        return redirect(url_for("main.payment_link_creation_failed"))

    data = {
        **form_data,
        "id": id,
        "payment_id": payment_id,
        "created_at": datetime.now(),
    }

    add_service_record_request(data)

    return redirect(payment_url)


@bp.route("/handle-gov-uk-pay-response/")
def handle_gov_uk_pay_response():
    id = request.args.get("id")
    response_type = request.args.get("response_type")

    if not id or not response_type:
        # User got here without ID - likely manually, do something... (redirect to form?)
        return "Shouldn't be here"

    if response_type == "request":
        gov_uk_payment_id = get_payment_id_from_record_id(id)
    elif response_type == "payment":
        payment = get_gov_uk_dynamics_payment(id)
        gov_uk_payment_id = payment.gov_uk_payment_id if payment else None

    if gov_uk_payment_id is None:
        # User got here with an ID that doesn't exist in the DB - could be our fault, or could be malicious, do something
        return "Shouldn't be here"
    
    gov_uk_payment_data = get_payment_data(gov_uk_payment_id)
    
    if gov_uk_payment_data is None:
        # Could not retrieve payment data from GOV.UK Pay - log and inform user
        current_app.logger.error(f"Could not retrieve payment data for GOV.UK payment ID: {gov_uk_payment_id}")
        return "Some sort of error" # TODO: We need to make a proper error page for this to show we couldn't connect to GOV.UK Pay API - maybe provide the GOV.UK Pay ID and to contact webmaster?
    
    if validate_payment(gov_uk_payment_data):
        if response_type == "request":
            try:
                process_valid_request(gov_uk_payment_id)
            except Exception as e:
                current_app.logger.error(
                    f"Error processing valid request of payment ID {gov_uk_payment_id}: {e}"
                )
        elif response_type == "payment":
            try:
                process_valid_payment(payment.id)
            except Exception as e:
                current_app.logger.error(
                    f"Error processing valid payment of payment ID {gov_uk_payment_id}: {e}"
                )

        return redirect(url_for("main.confirm_payment_received"))

    # Let the user know it failed, ask if they want to retry
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


@bp.route("/create-payment/", methods=["POST"])
def create_payment_endpoint():
    """
    Required params:
    - case_number
    - reference
    - net_amount
    - payee_email

    Optional params:
    - delivery_amount
    - first_name
    - last_name
    - details
    """
    data = request.json
    required = ["case_number", "reference", "net_amount", "payee_email"]

    if missing := [field for field in required if field not in data]:
        return {"error": f"Missing required fields: {', '.join(missing)}"}, 400

    try:
        data["net_amount"] = int(data["net_amount"]*100)  # Convert to pence
        if data["net_amount"] <= 0:
            return {"error": "Net amount must be greater than zero"}, 400
    except (ValueError, TypeError):
        return {"error": "Invalid net amount format"}, 400
    
    if "delivery_amount" in data:
        try:
            data["delivery_amount"] = int(data["delivery_amount"]*100)  # Convert to pence
            if data["delivery_amount"] <= 0:
                return {"error": "Delivery amount must be greater than zero"}, 400
        except (ValueError, TypeError):
            return {"error": "Invalid delivery amount format"}, 400

    # Exclude any extra fields to avoid unexpected errors
    data = {
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

    try:
        payment = add_dynamics_payment(data)
        if payment is None:
            return {"error": "Failed to create payment"}, 500
    except Exception as e:
        current_app.logger.error(f"Error creating payment: {e}")
        return {"error": "Failed to create payment"}, 500

    send_email(
        to=data["payee_email"],
        subject="Payment for Service Record Request",
        body=f"You have been requested to make a payment for a service record request. Please visit the following link to complete your payment: {url_for('main.make_payment', id=payment, _external=True)}",
    )

    return {"message": f"Payment created and sent successfully: {payment}"}, 201


@bp.route("/payment/<id>/", methods=["GET", "POST"])
def make_payment(id):
    form = ProceedToPay()
    payment = get_dynamics_payment(id)
    content = load_content()

    if payment is None:
        return "Payment not found"

    if form.validate_on_submit():
        return redirect(url_for("main.gov_uk_pay_redirect", id=payment.id))

    return render_template(
        "main/payment/dynamics-payment.html",
        form=form,
        payment=payment,
        content=content,
    )


@bp.route("/payment-redirect/<id>/", methods=["GET"])
def gov_uk_pay_redirect(id):
    payment = get_dynamics_payment(id)

    if payment is None:
        return "Payment not found"

    id = str(uuid.uuid4())

    response = create_payment(
        amount=payment.total_amount,
        description=f"{payment.case_number}{': ' + payment.details if payment.details else ''}",
        reference=payment.reference,
        email=payment.payee_email,
        return_url=f"{url_for("main.handle_gov_uk_pay_response", _external=True)}?id={id}&response_type=payment",
    )

    if not response:
        return redirect(url_for("main.payment_link_creation_failed"))

    gov_uk_payment_url = response.get("_links", {}).get("next_url", "").get("href", "")
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
