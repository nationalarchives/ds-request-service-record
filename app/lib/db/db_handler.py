from app.constants import ServiceBranches
from app.lib.db.models import (
    DynamicsPayment,
    GOVUKDynamicsPayment,
    ServiceRecordRequest,
    db,
)
from flask import current_app

from app.lib.price_calculations import get_delivery_type

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

def get_service_record_request(id: str = None) -> ServiceRecordRequest | None:
    """
    Get a ServiceRecordRequest item by its ID.
    """
    try:
        record = db.session.get(ServiceRecordRequest, id)
    except Exception as e:
        current_app.logger.error(f"Error fetching service record request: {e}")
        return None

    if not record:
        current_app.logger.error(f"Service record not found for ID: {id}")

    return record


def get_gov_uk_payment_id_from_record_id(id: str) -> str | None:
    record = get_service_record_request(id=id)
    return record.gov_uk_payment_id if record else None


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


def delete_service_record_request(record: ServiceRecordRequest) -> bool:
    try:
        db.session.delete(record)
        db.session.commit()
        return True
    except Exception as e:
        current_app.logger.error(f"Error deleting service record request: {e}")
        db.session.rollback()
        return False


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


def add_gov_uk_dynamics_payment(data: dict) -> GOVUKDynamicsPayment | None:
    try:
        payment = GOVUKDynamicsPayment(**data)
        db.session.add(payment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error adding GOV.UK dynamics payment: {e}")
        db.session.rollback()
    return payment


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
    """
    Transform form data into ServiceRecordRequest format.
    
    Filters fields to only include those that exist on ServiceRecordRequest model,
    and normalizes certain field values for database storage.
    
    Args:
        form_data: Dictionary of form field values.
        
    Returns:
        dict: Transformed data ready for ServiceRecordRequest creation.
    """
    # Filter to only valid ServiceRecordRequest fields
    transformed_data = {
        field: value
        for field, value in form_data.items()
        if hasattr(ServiceRecordRequest, field)
    }

    transformed_data["delivery_type"] = get_delivery_type(form_data)

    if service_branch := form_data.get("service_branch"):
        if service_branch in ServiceBranches.__members__:
            transformed_data["service_branch"] = ServiceBranches[service_branch].value
            
    return transformed_data
