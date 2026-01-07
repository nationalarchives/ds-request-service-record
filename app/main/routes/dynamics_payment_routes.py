import uuid
from datetime import datetime

from app.lib.aws import send_email
from app.lib.content import load_content
from app.lib.db.constants import (
    PAID_STATUS,
    SENT_STATUS,
)
from app.lib.db.db_handler import (
    add_dynamics_payment,
    add_gov_uk_dynamics_payment,
    delete_dynamics_payment,
    get_dynamics_payment,
)
from app.lib.db.models import db
from app.lib.gov_uk_pay import (
    create_payment,
)
from app.main import bp
from app.main.forms.proceed_to_pay import ProceedToPay
from flask import current_app, redirect, render_template, request, url_for


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

    gov_uk_dynamics_payment = add_gov_uk_dynamics_payment(data)

    if not gov_uk_dynamics_payment:
        return redirect(url_for("main.payment_link_creation_failed"))

    return redirect(gov_uk_payment_url)


@bp.route("/payment/<id>/", methods=["GET", "POST"])
def make_payment(id):
    payment = get_dynamics_payment(id)

    if payment is None:
        return "Payment not found"

    if payment.status == PAID_STATUS:
        return render_template("errors/payment_already_processed.html"), 400

    form = ProceedToPay()
    content = load_content()

    if form.validate_on_submit():
        return redirect(url_for("main.gov_uk_pay_redirect", id=payment.id))

    return render_template(
        "main/payment/dynamics-payment.html",
        form=form,
        payment=payment,
        content=content,
    )


def _validate_and_convert_amount(
    amount_value: float | int | str, field_name: str
) -> tuple:
    """
    Validate and convert an amount to pence.

    Args:
        amount_value: The amount value to validate (can be float, int, or string)
        field_name: The name of the field for error messages

    Returns:
        tuple: (converted_amount_in_pence, error_response) where error_response is None if valid
    """
    try:
        amount = float(amount_value)
        if round(amount, 2) != amount:
            return None, (
                {"error": f"{field_name} cannot have more than 2 decimal places"},
                400,
            )

        amount_in_pence = int(amount * 100)  # Convert to pence
        if field_name == "net_amount" and amount_in_pence <= 0:
            return None, ({"error": f"{field_name} must be greater than zero"}, 400)
        elif field_name == "delivery_amount" and amount_in_pence < 0:
            return None, ({"error": f"{field_name} must be zero or greater"}, 400)

        return amount_in_pence, None
    except (ValueError, TypeError):
        return None, ({"error": f"Invalid {field_name} format"}, 400)


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
    required_fields = ["case_number", "reference", "net_amount", "payee_email"]

    if missing := [field for field in required_fields if field not in data]:
        return {"error": f"Missing required fields: {', '.join(missing)}"}, 400

    net_amount, error = _validate_and_convert_amount(data["net_amount"], "net_amount")

    if error:
        return error

    data["net_amount"] = net_amount

    if "delivery_amount" in data:
        delivery_amount, error = _validate_and_convert_amount(
            data["delivery_amount"], "delivery_amount"
        )

        if error:
            return error

        data["delivery_amount"] = delivery_amount

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

    payment = add_dynamics_payment(data)

    if payment is None:
        return {"error": "Failed to create payment"}, 500

    try:
        payment.status = SENT_STATUS
        db.session.commit()
    except Exception as e:
        current_app.logger.error(
            f"Error updating payment status for payment {payment.id}: {e}, deleting payment record."
        )
        delete_dynamics_payment(payment)
        return {"error": "Failed to create payment"}, 500

    if send_email(
        to=data["payee_email"],
        subject="Payment for Service Record Request",
        body=f"You have been requested to make a payment for a service record request. Please visit the following link to complete your payment: {url_for('main.make_payment', id=payment.id, _external=True)}",
    ):
        return {"message": f"Payment created and sent successfully: {payment.id}"}, 201
    else:
        current_app.logger.error(
            f"Error sending payment email for payment {payment.id}. Deleting payment."
        )
        delete_dynamics_payment(payment)
        return {"error": "Failed to send payment email"}, 500
