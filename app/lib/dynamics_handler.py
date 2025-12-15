"""
Dynamics integration module.

This module handles communication with Microsoft Dynamics and MOD Copying app,
including sending service record requests and payment information.
"""

from datetime import datetime

import requests

from app.lib.aws import send_email
from app.lib.models import DynamicsPayment, ServiceRecordRequest
from flask import current_app

# Currency conversion constant
PENCE_TO_POUNDS_DIVISOR = 100

# Age threshold for open records (115+ years old)
AGE_THRESHOLD_OPEN = 115

# Mapping of Dynamics field names to ServiceRecordRequest attributes
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


def send_request_to_dynamics(record: ServiceRecordRequest) -> None:
    """
    Send a service record request to Dynamics via email.
    
    Args:
        record: ServiceRecordRequest instance to send.
    """
    send_email(
        to=current_app.config["DYNAMICS_INBOX"],
        subject=subject_status(record),
        body=generate_tagged_request(record),
    )


def _determine_closure_status(record: ServiceRecordRequest, age: int) -> str:
    """
    Determine the FOI closure status code based on age and proof of death.
    
    Args:
        record: ServiceRecordRequest instance.
        age: Age calculated from date of birth.
        
    Returns:
        str: Closure status code (FOIOP, FOICD, or FOICDN).
    """
    if age >= AGE_THRESHOLD_OPEN:
        return "FOIOP"
    
    return "FOICD" if record.proof_of_death else "FOICDN"


def subject_status(record: ServiceRecordRequest) -> str:
    """
    Generate email subject line for Dynamics based on record details.
    
    The subject includes FOI status and processing option.
    
    Args:
        record: ServiceRecordRequest instance.
        
    Returns:
        str: Email subject line.
    """
    dob = datetime.strptime(record.date_of_birth, "%d %B %Y")
    age = datetime.now().year - dob.year

    closure_status = _determine_closure_status(record, age)
    option = "1" if record.processing_option == "standard" else "2"
    
    return f"? FOI DIRECT MOD {closure_status}{option}"


def _build_payment_payload(payment: DynamicsPayment) -> dict:
    """
    Build the payload for MOD Copying API from payment data.
    
    Args:
        payment: DynamicsPayment instance.
        
    Returns:
        dict: Payload for MOD Copying API request.
    """
    return {
        "CaseNumber": payment.case_number,
        "PayReference": payment.reference,
        "GovUkProviderId": payment.provider_id,
        "Amount": payment.total_amount / PENCE_TO_POUNDS_DIVISOR,
        "Date": payment.payment_date.strftime("%Y-%m-%d"),
    }


def send_payment_to_mod_copying_app(payment: DynamicsPayment) -> None:
    """
    Send payment information to MOD Copying application.
    
    Args:
        payment: DynamicsPayment instance to send.
        
    Raises:
        ValueError: If the API request fails.
    """
    payload = _build_payment_payload(payment)

    try:
        response = requests.post(
            current_app.config["MOD_COPYING_API_URL"],
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        current_app.logger.error(
            f"Failed to update MOD Copying app for payment ID {payment.id}: {e}"
        )
        raise ValueError("Could not update MOD Copying app with payment details") from e


def _generate_tagged_data(mapping: list[tuple[str, str | None]], obj) -> str:
    """
    Generate XML-tagged data from object attributes.
    
    Args:
        mapping: List of tuples mapping tag names to object attributes.
        obj: Object to extract attribute values from.
        
    Returns:
        str: XML-tagged string with object data.
    """
    chunks = []
    for tag, attr in mapping:
        value = getattr(obj, attr) if attr else None
        if value:
            text = str(value)
            chunks.append(f"<{tag}>{text}</{tag}>")
    return "\n".join(chunks)


def generate_tagged_request(record: ServiceRecordRequest) -> str:
    """
    Generate tagged XML string for a service record request.
    
    Args:
        record: ServiceRecordRequest instance.
        
    Returns:
        str: XML-tagged representation of the record.
    """
    return _generate_tagged_data(DYNAMICS_REQUEST_FIELD_MAP, record)
