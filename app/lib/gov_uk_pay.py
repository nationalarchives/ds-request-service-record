import hashlib
import hmac
from enum import Enum

import requests
from app.lib.db_handler import delete_service_record_request, get_service_record_request
from app.lib.dynamics_handler import send_data_to_dynamics
from flask import current_app


class GOV_UK_PAY_EVENT_TYPES(Enum):
    EXPIRED = "card_payment_expired"
    CANCELLED = "card_payment_cancelled"
    SUCCEEDED = "card_payment_succeeded"


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


def is_webhook_signature_valid(request: requests.Request) -> bool:
    signing_secret = current_app.config["GOV_UK_PAY_SIGNING_SECRET"]
    pay_signature = request.headers.get("Pay-Signature", "")
    body = request.get_data()

    hmac_obj = hmac.new(signing_secret.encode("utf-8"), body, hashlib.sha256)

    generated_signature = hmac_obj.hexdigest()

    if pay_signature != generated_signature:
        return False

    return True


def process_webhook_data(data: dict) -> None:
    payment_id = data.get("resource_id", "")
    event_type = data.get("event_type", "")

    record = get_service_record_request(payment_id)

    if record is None:
        raise ValueError(f"Service record not found for payment ID: {payment_id}")

    if event_type not in [type.value for type in GOV_UK_PAY_EVENT_TYPES]:
        raise ValueError(f"Unknown event type received: {event_type}")

    if event_type == GOV_UK_PAY_EVENT_TYPES.SUCCEEDED.value:
        send_data_to_dynamics(record)

    delete_service_record_request(record)
