from datetime import datetime
from enum import Enum

import requests
from app.lib.db import (
    db,
    NEW_STATUS,
    PAID_STATUS,
    SENT_STATUS,
    get_dynamics_payment,
    get_gov_uk_dynamics_payment,
    get_service_record_request,
)
from app.lib.dynamics_handler import (
    send_payment_to_mod_copying_app,
    send_request_to_dynamics,
)
from flask import current_app

SUCCESSFUL_PAYMENT_STATUSES: set[str] = {"success"}

UNFINISHED_PAYMENT_STATUSES: set[str] = {"created", "started", "submitted"}

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


def get_payment_status(data: dict) -> str:
    return data.get("state", {}).get("status")


def validate_payment(data: dict) -> bool:
    return get_payment_status(data) == "success"


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
        "reference": reference,
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


def process_valid_request(id: str, payment_data: dict) -> None:
    record = get_service_record_request(record_id=id)

    if record is None:
        raise ValueError(f"Service record not found for payment ID: {id}")

    if record.status == NEW_STATUS:
        record.provider_id = payment_data.get("provider_id", None)
        record.amount_received = (
            f"{payment_data.get('amount') / 100:.2f}"
            if payment_data.get("amount") is not None
            else None
        )
        record.payment_reference = payment_data.get("reference", "")
        record.payment_date = datetime.now().strftime("%d %B %Y")
        record.status = PAID_STATUS
        db.session.commit()

    if record.status == PAID_STATUS:
        if send_request_to_dynamics(record):
            record.status = SENT_STATUS
            db.session.commit()


def process_valid_payment(id: str, *, provider_id: str, payment_date: str) -> None:
    payment = get_dynamics_payment(id)

    if payment is None:
        raise ValueError(f"Payment not found for payment ID: {id}")

    payment.status = PAID_STATUS
    payment.provider_id = provider_id
    payment.payment_date = datetime.strptime(payment_date, "%Y-%m-%d")
    db.session.commit()

    send_payment_to_mod_copying_app(payment)
