from datetime import datetime

import requests
from app.lib.api import JSONAPIClient
from app.lib.aws import move_proof_of_death_to_submitted
from app.lib.db.constants import (
    NEW_STATUS,
    PAID_STATUS,
    SENT_STATUS,
)
from app.lib.db.db_handler import (
    get_dynamics_payment,
    get_service_record_request,
)
from app.lib.db.models import db
from app.lib.dynamics_handler import (
    send_payment_to_mod_copying_app,
    send_request_to_dynamics,
)
from flask import current_app

SUCCESSFUL_PAYMENT_STATUSES: set[str] = {"success"}

UNFINISHED_PAYMENT_STATUSES: set[str] = {"created", "started", "submitted"}

FAILED_PAYMENT_STATUSES: set[str] = {"failed", "cancelled", "error"}


class GOVUKPayAPIClient(JSONAPIClient):
    data = None

    def __init__(self):
        super().__init__(
            api_url=current_app.config["GOV_UK_PAY_API_URL"],
            headers={
                "Authorization": f"Bearer {current_app.config['GOV_UK_PAY_API_KEY']}",
                "Content-Type": "application/json",
            },
        )

    def get_payment(self, payment_id: str) -> dict:
        self.data = self.get(path=f"/{payment_id}")
        return self.data

    def get_payment_status(self) -> str | None:
        if self.data is None:
            return None
        return self.data.get("state", {}).get("status")

    def is_payment_successful(self) -> bool:
        status = self.get_payment_status()
        return status in SUCCESSFUL_PAYMENT_STATUSES


def create_payment(
    amount: int, description: str, reference: str, email: str | None, return_url: str
) -> dict | None:
    headers = {
        "Authorization": f"Bearer {current_app.config['GOV_UK_PAY_API_KEY']}",
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
        current_app.logger.error(f"Error creating payment: {e}: {response.text}")
        return None

    return response.json()


def process_valid_request(id: str, payment_data: dict) -> None:
    record = get_service_record_request(id=id)

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

    if record.proof_of_death and record.proof_of_death != "EMPTY":
        if not move_proof_of_death_to_submitted(record.proof_of_death):
            current_app.logger.warning(
                "Failed to move proof of death file to submitted bucket."
            )

    if record.status == PAID_STATUS:
        if send_request_to_dynamics(record):
            record.status = SENT_STATUS
            db.session.commit()


def process_valid_payment(id: str, *, provider_id: str) -> None:
    payment = get_dynamics_payment(id)

    if payment is None:
        raise ValueError(f"Payment not found for payment ID: {id}")

    payment.status = PAID_STATUS
    payment.provider_id = provider_id
    payment.payment_date = datetime.now()
    db.session.commit()

    send_payment_to_mod_copying_app(payment)
