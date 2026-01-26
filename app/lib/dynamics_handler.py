from datetime import datetime

import requests
from app.lib.aws import send_email
from app.lib.db.models import DynamicsPayment, ServiceRecordRequest
from flask import current_app

DYNAMICS_REQUEST_FIELD_MAP = [
    ("mandatory_forename", "requester_first_name"),
    ("mandatory_surname", "requester_last_name"),
    ("mandatory_email", "requester_email"),
    ("mandatory_address1", "requester_address1"),
    ("address2", "requester_address2"),
    ("mandatory_town", "requester_town_city"),
    ("county", "requester_county"),
    ("postcode", "requester_postcode"),
    ("mandatory_country", "requester_country"),
    ("mandatory_certificate_forename", "forenames"),
    ("mandatory_certificate_surname", "last_name"),
    ("mandatory_birth_date", "date_of_birth"),
    ("birth_place", "place_of_birth"),
    ("service_number", "service_number"),
    ("regiment", "regiment"),
    ("mandatory_upload_file_name", "proof_of_death"),
    ("enquiry", "additional_information"),
    (
        "mandatory_catalogue_reference",
        "catalogue_reference",
    ),
    ("certificate_othernames", "other_last_names"),
    ("date_of_death", "date_of_death"),
    ("mod_barcode_number", "mod_reference"),
    ("service_branch", "service_branch"),
    ("died_in_service", "died_in_service"),
    ("prior_contact_reference", "case_reference_number"),
    ("payment_date", "payment_date"),
    ("delivery_type", "delivery_type"),
    ("process_type", "processing_option"),
    ("payment_reference", "payment_reference"),
    ("amount_received", "amount_received"),
    ("provider_id", "provider_id"),
]

class DynamicsClosureStatus:
    FOIOP = "FOIOP"   # Open record - Over 115
    FOICD = "FOICD"   # Closed record - Proof of Death provided
    FOICDN = "FOICDN" # Closed record - No Proof of Death provided


def send_request_to_dynamics(record: ServiceRecordRequest) -> bool:
    return send_email(
        to=current_app.config["DYNAMICS_INBOX"],
        subject=subject_status(record),
        body=generate_tagged_request(record),
    )


def closure_status_calculation(date_of_birth: str, has_proof_of_death: bool) -> str:
    dob = datetime.strptime(date_of_birth, "%d %B %Y")
    age = datetime.now().year - dob.year

    if age >= 115:
        closure_status = DynamicsClosureStatus.FOIOP
    else:
        if has_proof_of_death:
            closure_status = DynamicsClosureStatus.FOICD
        else:
            closure_status = DynamicsClosureStatus.FOICDN

    return closure_status


def has_proof_of_death(record: ServiceRecordRequest) -> bool:
    if record.proof_of_death and record.proof_of_death != "EMPTY":
        return True
    return False


def subject_status(record: ServiceRecordRequest) -> str:
    closure_status = closure_status_calculation(
        date_of_birth=record.date_of_birth,
        has_proof_of_death=has_proof_of_death(record),
    )

    option = "1" if record.processing_option == "standard" else "2"
    return f"? FOI DIRECT MOD {closure_status}{option}"


def send_payment_to_mod_copying_app(payment: DynamicsPayment) -> None:
    payload = {
        "CaseNumber": payment.case_number,
        "PayReference": payment.reference,
        "GovUkProviderId": payment.provider_id,
        "Amount": (payment.total_amount / 100),
        "Date": payment.payment_date.strftime("%Y-%m-%d"),
    }

    response = requests.post(
        current_app.config["MOD_COPYING_API_URL"],
        json=payload,
        headers={"Content-Type": "application/json"},
    )

    if response.status_code != 200:
        current_app.logger.error(
            f"Failed to update MOD Copying app for payment ID {payment.id}: {response.status_code} - {response.text}"
        )
        raise ValueError("Could not update MOD Copying app with payment details")


def _generate_tagged_data(mapping: list[tuple[str, str | None]], obj) -> str:
    chunks = []
    for tag, attr in mapping:
        # If mandatory_upload_file_name is missing, insert the placeholder text
        # Dynamics has this as a required field so we must provide something here
        if tag != "mandatory_upload_file_name":
            value = getattr(obj, attr) if attr else None
            if value:
                text = str(value)
                chunks.append(f"<{tag}>{text}</{tag}>")
        else:
            if closure_status_calculation(obj.date_of_birth, has_proof_of_death(obj)) != DynamicsClosureStatus.FOIOP:
                value = getattr(obj, attr) if attr else None
                if value:
                    text = str(value)
                    if text != "EMPTY":
                        chunks.append(f"<{tag}>{text}</{tag}>")
            else:
                chunks.append(f"<{tag}>Not applicable</{tag}>")
    return "\n".join(chunks)


def generate_tagged_request(record: ServiceRecordRequest) -> str:
    return _generate_tagged_data(DYNAMICS_REQUEST_FIELD_MAP, record)
