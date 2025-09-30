import uuid
from datetime import datetime

from app.lib.aws import upload_proof_of_death
from app.lib.content import load_content
from app.lib.db_handler import add_dynamics_payment, add_service_record_request, get_payment_id_from_record_id
from app.lib.gov_uk_pay import (
    create_payment,
    process_valid_request,
    process_webhook_data,
    validate_payment,
    validate_webhook_signature,
)
from app.main import bp
from app.main.forms.proceed_to_pay import ProceedToPay
from app.main.forms.request_a_service_record import RequestAServiceRecord
from flask import current_app, redirect, render_template, request, session, url_for


@bp.route("/all-fields-in-one-form/", methods=["GET", "POST"])
def all_fields_in_one_form():
    form = RequestAServiceRecord()
    content = load_content()

    if form.validate_on_submit():
        session["form_data"] = {}
        for field_name, field in form._fields.items():
            if field_name not in ["csrf_token", "submit"]:
                if field_name == "evidence_of_death":
                    if data := field.data:
                        file = upload_proof_of_death(file=data)

                        if file is None:
                            # Redirect back to file upload form with error message "file failed to upload, try again"
                            return redirect(url_for("main.all_fields_in_one_form"))

                        session["form_data"][field_name] = file if file else None
                else:
                    session["form_data"][field_name] = field.data

        return redirect(url_for("main.review"))

    return render_template(
        "main/all-fields-in-one-form/form.html", content=content, form=form
    )


@bp.route("/review/", methods=["GET", "POST"])
def review():
    content = load_content()
    form = ProceedToPay()
    form_data = session.get("form_data", {})

    if form.validate_on_submit():
        return redirect(url_for("main.send_to_gov_pay"))

    return render_template(
        "main/all-fields-in-one-form/review.html",
        form=form,
        form_data=form_data,
        content=content,
    )


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
        return_url=f"{url_for("main.handle_gov_uk_pay_response", _external=True)}?id={id}",
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

    if not id:
        # User got here without ID - likely manually, do something... (redirect to form?)
        return "Shouldn't be here"

    payment_id = get_payment_id_from_record_id(id)

    if payment_id is None:
        # User got here with an ID that doesn't exist in the DB - could be our fault, or could be malicious, do something
        return "Shouldn't be here"

    if validate_payment(payment_id):
        try:
            process_valid_request(payment_id)
        except Exception as e:
            current_app.logger.error(
                f"Error processing valid request of payment ID {payment_id}: {e}"
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


@bp.route("/gov-uk-pay-webhook/", methods=["POST"])
def gov_uk_pay_webhook():

    if not validate_webhook_signature(request):
        return "FAILED", 403

    try:
        process_webhook_data(request.json)
    except Exception as e:
        current_app.logger.error(f"Error processing webhook data: {e}")
        return "FAILED", 500

    return "SUCCESS", 200


@bp.route("/create-payment/", methods=["POST"])
def create_payment_endpoint():
    data = request.json
    required = ["amount", "description", "reference", "payee_email"]

    if missing := [field for field in required if field not in data]:
        return {"error": f"Missing required fields: {', '.join(missing)}"}, 400

    try:
        data["amount"] = int(data["amount"])
        if data["amount"] <= 0:
            return {"error": "Amount must be greater than zero"}, 400
    except (ValueError, TypeError):
        return {"error": "Invalid amount format"}, 400
    
    # Exclude any extra fields to avoid unexpected errors
    data = {
        "amount": data["amount"],
        "description": data["description"],
        "reference": data["reference"],
        "payee_email": data["payee_email"],
    }

    try:
        payment = add_dynamics_payment(data)
        if payment is None:
            return {"error": "Failed to create payment"}, 500
    except:
        return {"error": "Failed to create payment"}, 500

    return {"message": f"Payment created successfully: {payment}"}, 201