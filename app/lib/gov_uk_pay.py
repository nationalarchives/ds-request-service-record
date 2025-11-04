from datetime import datetime
from enum import Enum

import requests
from app.lib.db_handler import (
    delete_service_record_request,
    get_dynamics_payment,
    get_gov_uk_dynamics_payment,
    get_service_record_request,
)
from app.lib.dynamics_handler import send_payment_to_dynamics, send_request_to_dynamics
from app.lib.models import db
from flask import current_app


class GOV_UK_PAY_EVENT_TYPES(Enum):
    EXPIRED = "card_payment_expired"
    FAILED = "card_payment_failed"
    SUCCEEDED = "card_payment_succeeded"


FAILED_PAYMENT_STATUSES: set[str] = {"failed", "cancelled", "error"}


def get_payment_data(payment_id: str) -> dict | None:
    headers = {
        "Authorization": f"Bearer {current_app.config["GOV_UK_PAY_API_KEY"]}",
        "Content-Type": "application/json",
    }

    response = requests.get(
        f"{current_app.config["GOV_UK_PAY_API_URL"]}/{payment_id}", headers=headers
    )

    try:
        response.raise_for_status()
    except Exception as e:
        current_app.logger.error(f"Error fetching payment data: {e}")
        return None

    return response.json()


def validate_payment(data: dict) -> bool:
    return data.get("state", {}).get("status") == "success"


def create_payment(
    amount: int, description: str, reference: str, email: str | None, return_url: str
) -> dict | None:
    headers = {
        "Authorization": f"Bearer {current_app.config["GOV_UK_PAY_API_KEY"]}",
        "Content-Type": "application/json",
    }

    payload = {
        "amount": amount,
        "description": description,
        "reference": reference,  # TODO: Investigate the dynamic reference that other/current services use (TNA-xxxxx?)
        "return_url": return_url,
    }

    if email is not None:
        payload["email"] = email

    response = requests.post(
        current_app.config["GOV_UK_PAY_API_URL"], json=payload, headers=headers
    )

    try:
        response.raise_for_status()
    except Exception as e:
        current_app.logger.error(f"Error creating payment: {e}")
        return None

    return response.json()


def process_valid_request(payment_id: str, payment_data: dict) -> None:
    record = get_service_record_request(payment_id=payment_id)

    record.provider_id = payment_data.get("provider_id", None)
    record.amount_received = payment_data.get("amount", None)
    record.payment_reference = payment_data.get("reference", "")
    record.payment_date = datetime.now()
    db.session.commit()

    if record is None:
        raise ValueError(f"Service record not found for payment ID: {payment_id}")

    send_request_to_dynamics(record)

    delete_service_record_request(record)


def process_valid_payment(id: str, provider_id: str) -> None:
    payment = get_gov_uk_dynamics_payment(id)

    if payment is None:
        raise ValueError(f"Payment not found for GOV.UK payment ID: {id}")

    get_dynamics_payment(payment.dynamics_payment_id).status = "P"
    get_dynamics_payment(payment.dynamics_payment_id).provider_id = provider_id
    db.session.commit()

    send_payment_to_dynamics(get_dynamics_payment(payment.dynamics_payment_id))
