from app.lib.aws import send_email
from app.lib.models import ServiceRecordRequest
from flask import current_app

DYNAMICS_FIELD_MAP = [
    ("enquiry_id", "id"),
    ("title", "requester_title"),
    ("mandatory_forename", "requester_first_name"),
    ("mandatory_surname", "requester_last_name"),
    ("mandatory_email", "requester_email"),
    ("mandatory_address1", "requester_address1"),
    ("address2", "requester_address2"),
    ("address3", None),  # TODO: no source yet
    ("mandatory_town", "requester_town_city"),
    ("county", "requester_county"),
    ("mandatory_postcode", "requester_postcode"),
    ("mandatory_country", "requester_country"),
    ("mandatory_certificate_forename", "forenames"),
    ("mandatory_certificate_surname", "lastname"),
    ("mandatory_birth_date", "date_of_birth"),
    ("birth_place", "place_of_birth"),
    ("service_number", "service_number"),
    ("regiment", "regiment"),
    ("mandatory_upload_file_name", "evidence_of_death"),
    ("enquiry", "additional_information"),
    (
        "mandatory_catalogue_reference",
        None,
    ),  # TODO: this comes automatically from the catalogue, currently
    ("certificate_othernames", "other_last_names"),
    ("date_of_death", "date_of_death"),
    ("mod_barcode_number", "mod_reference"),
    ("service_branch", "service_branch"),
    ("died_in_service", "died_in_service"),
    ("prior_contact_reference", "case_reference_number"),
]


def send_data_to_dynamics(record: ServiceRecordRequest) -> None:
    # Check "status" of record, based on defined logic (used in Dynamics email subject, e.g. FOICD, DPA, etc)

    tagged_data = generate_tagged_data(record)

    send_email(
        to=current_app.config["DYNAMICS_INBOX"],
        subject=f"New Service Record Request: {record.id}",
        body=tagged_data,
    )


def generate_tagged_data(record: ServiceRecordRequest) -> str:
    chunks = []
    for tag, attr in DYNAMICS_FIELD_MAP:
        value = getattr(record, attr) if attr else None
        if value:
            text = str(value)
            chunks.append(f"<{tag}>{text}</{tag}>")
    return "\n".join(chunks)
