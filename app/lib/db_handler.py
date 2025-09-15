from app.lib.models import ServiceRecordRequest, db
from flask import current_app


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
            f"Service record not found for payment_id: {payment_id}"
        )

    return record


def get_payment_id_from_record_id(record_id: str) -> str | None:
    record = get_service_record_request(record_id=record_id)
    return record.payment_id if record else None


def add_service_record_request(data: dict) -> None:
    try:
        record = ServiceRecordRequest(**data)
        db.session.add(record)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error adding service record request: {e}")
        db.session.rollback()


def delete_service_record_request(record: ServiceRecordRequest) -> None:
    try:
        db.session.delete(record)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error deleting service record request: {e}")
        db.session.rollback()
