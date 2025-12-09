from app.constants import ServiceBranches
from app.lib.models import (
    DynamicsPayment,
    GOVUKDynamicsPayment,
    ServiceRecordRequest,
    db,
)
from flask import current_app


def hash_check(record_hash: str) -> ServiceRecordRequest | None:
    """
    Check if a ServiceRecordRequest with the given hash already exists, return the record if found.
    """
    try:
        existing_record = (
            db.session.query(ServiceRecordRequest)
            .filter_by(record_hash=record_hash)
            .first()
        )
        if existing_record:
            current_app.logger.info(
                f"Duplicate record detected with hash: {record_hash}"
            )
            return existing_record
        return None
    except Exception as e:
        current_app.logger.error(f"Error checking record hash: {e}")
        return None        
    

def get_service_record_request(
    *, payment_id: str | None = None, record_id: str | None = None
) -> ServiceRecordRequest | None:
    """
    Get a ServiceRecordRequest item by payment_id or record_id.
    Must provide either a payment_id OR a record_id.
    """
    if (payment_id is None and record_id is None) or (
        payment_id is not None and record_id is not None
    ):
        raise ValueError("Invalid parameters: provide either payment_id or record_id.")

    try:
        if record_id is not None:
            record = db.session.get(ServiceRecordRequest, record_id)
        else:
            record = (
                db.session.query(ServiceRecordRequest)
                .filter_by(payment_id=payment_id)
                .first()
            )
    except Exception as e:
        current_app.logger.error(f"Error fetching service record request: {e}")
        return None

    if not record:
        current_app.logger.error(
            f"Service record not found for: {payment_id or record_id}"
        )

    return record


def get_payment_id_from_record_id(record_id: str) -> str | None:
    record = get_service_record_request(record_id=record_id)
    return record.payment_id if record else None


def add_service_record_request(data: dict) -> ServiceRecordRequest | None:
    record = None
    try:
        record = ServiceRecordRequest(**data)
        db.session.add(record)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error adding service record request: {e}")
        db.session.rollback()
    return record


def delete_service_record_request(record: ServiceRecordRequest) -> None:
    try:
        db.session.delete(record)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error deleting service record request: {e}")
        db.session.rollback()


def get_dynamics_payment(id: str) -> DynamicsPayment | None:
    try:
        payment = db.session.get(DynamicsPayment, id)
        if not payment:
            current_app.logger.error(f"Dynamics payment not found for ID: {id}")
        return payment
    except Exception as e:
        current_app.logger.error(f"Error fetching dynamics payment: {e}")
        return None


def add_dynamics_payment(data: dict) -> DynamicsPayment | None:
    try:
        payment = DynamicsPayment(**data)
        db.session.add(payment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error adding dynamics payment: {e}")
        db.session.rollback()

    return payment


def delete_dynamics_payment(record: DynamicsPayment) -> None:
    try:
        db.session.delete(record)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error deleting dynamics payment: {e}")
        db.session.rollback()


def add_gov_uk_dynamics_payment(data: dict) -> None:
    try:
        payment = GOVUKDynamicsPayment(**data)
        db.session.add(payment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error adding GOV.UK dynamics payment: {e}")
        db.session.rollback()


def get_gov_uk_dynamics_payment(id: str) -> GOVUKDynamicsPayment | None:
    try:
        payment = db.session.get(GOVUKDynamicsPayment, id)
        if not payment:
            current_app.logger.error(f"GOV UK payment not found for ID: {id}")
        return payment
    except Exception as e:
        current_app.logger.error(f"Error fetching GOV UK payment: {e}")
        return None


def transform_form_data_to_record(form_data: dict) -> dict:
    transformed_data = {
        field: value
        for field, value in form_data.items()
        if hasattr(ServiceRecordRequest, field)
    }

    if date_of_birth := form_data.get(
        "what_was_their_date_of_birth"
    ):  # TODO: can this field go back to `date_of_birth` in the frontend?
        transformed_data["date_of_birth"] = date_of_birth

    if form_data.get("processing_option") == "standard":
        delivery_type = form_data.get(
            "choose_your_order_type_standard_option"
        )
        if delivery_type == "printed":
            delivery_type = "PrintedTracked"
        else:
            delivery_type = "Digital"
        transformed_data["delivery_type"] = delivery_type
    elif form_data.get("processing_option") == "full":
        delivery_type = form_data.get(
            "choose_your_order_type_full_option"
        )
        if delivery_type == "printed":
            delivery_type = "PrintedTracked"
        else:
            delivery_type = "Digital"
        transformed_data["delivery_type"] = delivery_type

    if service_branch := form_data.get("service_branch"):
        if service_branch in ServiceBranches.__members__:
            transformed_data["service_branch"] = ServiceBranches[service_branch].value
    return transformed_data
