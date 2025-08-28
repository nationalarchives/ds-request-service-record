from flask import current_app
from app.lib.aws import send_email
from app.lib.models import ServiceRecordRequest


def send_data_to_dynamics(record: ServiceRecordRequest) -> None:
    # Check "status" of record, based on defined logic (used in Dynamics email subject, e.g. FOICD, DPA, etc)

    tagged_data = generate_tagged_data(record)

    send_email(
        to=current_app.config["DYNAMICS_INBOX"],
        subject=f"New Service Record Request: {record.id}",
        body=tagged_data
    )
    

def generate_tagged_data(record: ServiceRecordRequest) -> str:
    return f"""
        <enquiry_id>{record.id}</enquiry_id>
        <title>{record.requester_title}</title>
        <mandatory_forename>{record.requester_first_name}</mandatory_forename>
        <mandatory_surname>{record.requester_last_name}</mandatory_surname>
        <mandatory_email>{record.requester_email}</mandatory_email>
        <mandatory_address1>{record.requester_address1}</mandatory_address1>
        <address2>{record.requester_address2}</address2>
        <address3></address3>
        <mandatory_town>{record.requester_town_city}</mandatory_town>
        <county>{record.requester_county}</county>
        <mandatory_postcode>{record.requester_postcode}</mandatory_postcode>
        <mandatory_country>{record.requester_country}</mandatory_country>
        <mandatory_certificate_forename>{record.forenames}</mandatory_certificate_forename>
        <mandatory_certificate_surname>{record.lastname}</mandatory_certificate_surname>
        <mandatory_birth_date>{record.date_of_birth}</mandatory_birth_date>
        <birth_place>{record.place_of_birth}</birth_place>
        <service_number>{record.service_number}</service_number>
        <regiment>{record.regiment}</regiment>
        <mandatory_upload_file_name>{record.evidence_of_death}</mandatory_upload_file_name>
        <enquiry>{record.additional_information}</enquiry>
        <mandatory_catalogue_reference></mandatory_catalogue_reference>
        <certificate_othernames>{record.other_last_names}</certificate_othernames>
        <date_of_death>{record.date_of_death}</date_of_death>
        <mod_barcode_number>{record.service_number}</mod_barcode_number>
        <service_branch>{record.service_branch}</service_branch>
        <died_in_service>{record.died_in_service}</died_in_service>
        <prior_contact_reference>{record.case_reference_number}</prior_contact_reference>
    """