"""
GOV.UK Pay integration module.

This module handles payment operations with the GOV.UK Pay API including
creating payments, fetching payment data, and processing payment responses.
"""

from datetime import datetime
from enum import Enum

import requests
from app.lib.db_handler import (
    get_dynamics_payment,
    get_gov_uk_dynamics_payment,
    get_service_record_request,
)
from app.lib.dynamics_handler import (
    send_payment_to_mod_copying_app,
    send_request_to_dynamics,
)
from app.lib.models import db
from flask import current_app

# Payment status constants
SUCCESSFUL_PAYMENT_STATUSES: set[str] = {"success"}
UNFINISHED_PAYMENT_STATUSES: set[str] = {"created", "started", "submitted"}
FAILED_PAYMENT_STATUSES: set[str] = {"failed", "cancelled", "error"}

# Record status constants
RECORD_STATUS_NEW = "N"
RECORD_STATUS_PAID = "P"
RECORD_STATUS_SENT = "S"


class GovUKPayError(Exception):
    """Base exception for GOV.UK Pay related errors."""
    pass


def _get_auth_headers() -> dict[str, str]:
    """
    Create authorization headers for GOV.UK Pay API requests.
    
    Returns:
        dict: Headers with authorization and content type.
    """
    return {
        "Authorization": f"Bearer {current_app.config['GOV_UK_PAY_API_KEY']}",
        "Content-Type": "application/json",
    }


def get_payment_data(payment_id: str) -> dict | None:
    """
    Fetch payment data from GOV.UK Pay API.
    
    Args:
        payment_id: The GOV.UK Pay payment identifier.
        
    Returns:
        dict: Payment data from GOV.UK Pay API, or None if request fails.
    """
    try:
        response = requests.get(
            f"{current_app.config['GOV_UK_PAY_API_URL']}/{payment_id}",
            headers=_get_auth_headers(),
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error fetching payment data for {payment_id}: {e}")
        return None


def get_payment_status(data: dict) -> str | None:
    """
    Extract payment status from GOV.UK Pay response data.
    
    Args:
        data: Payment data dictionary from GOV.UK Pay API.
        
    Returns:
        str: Payment status, or None if not found.
    """
    return data.get("state", {}).get("status")


def validate_payment(data: dict) -> bool:
    """
    Check if payment has been successfully completed.
    
    Args:
        data: Payment data dictionary from GOV.UK Pay API.
        
    Returns:
        bool: True if payment is successful, False otherwise.
    """
    return get_payment_status(data) in SUCCESSFUL_PAYMENT_STATUSES


def create_payment(
    amount: int, 
    description: str, 
    reference: str, 
    email: str | None, 
    return_url: str
) -> dict | None:
    """
    Create a new payment with GOV.UK Pay.
    
    Args:
        amount: Payment amount in pence.
        description: Payment description.
        reference: Payment reference identifier.
        email: Optional email address for payment receipt.
        return_url: URL to redirect user after payment.
        
    Returns:
        dict: Payment creation response from GOV.UK Pay API, or None if request fails.
    """
    payload = {
        "amount": amount,
        "description": description,
        "reference": reference,
        "return_url": return_url,
    }

    if email is not None:
        payload["email"] = email

    try:
        response = requests.post(
            current_app.config["GOV_UK_PAY_API_URL"], 
            json=payload, 
            headers=_get_auth_headers(),
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error creating payment: {e}")
        return None


def _update_record_with_payment_data(record, payment_data: dict) -> None:
    """
    Update service record with payment information.
    
    Args:
        record: ServiceRecordRequest instance.
        payment_data: Payment data from GOV.UK Pay API.
    """
    record.provider_id = payment_data.get("provider_id")
    
    if amount := payment_data.get("amount"):
        record.amount_received = f"{amount / 100:.2f}"
    
    record.payment_reference = payment_data.get("reference", "")
    record.payment_date = datetime.now().strftime("%d %B %Y")
    record.status = RECORD_STATUS_PAID


def process_valid_request(payment_id: str, payment_data: dict) -> None:
    """
    Process a validated payment request and send to Dynamics.
    
    This function handles the state transitions from New -> Paid -> Sent.
    
    Args:
        payment_id: The GOV.UK Pay payment identifier.
        payment_data: Payment data from GOV.UK Pay API.
        
    Raises:
        ValueError: If service record is not found.
    """
    record = get_service_record_request(payment_id=payment_id)

    if record is None:
        raise ValueError(f"Service record not found for payment ID: {payment_id}")

    # Update record with payment data if still in 'New' status
    if record.status == RECORD_STATUS_NEW:
        _update_record_with_payment_data(record, payment_data)
        db.session.commit()

    # Send to Dynamics if in 'Paid' status
    if record.status == RECORD_STATUS_PAID:
        send_request_to_dynamics(record)
        record.status = RECORD_STATUS_SENT
        db.session.commit()


def process_valid_payment(id: str, *, provider_id: str, payment_date: str) -> None:
    """
    Process a validated payment for Dynamics integration.
    
    Updates the payment record and sends information to MOD Copying app.
    
    Args:
        id: The internal payment identifier.
        provider_id: Payment service provider identifier.
        payment_date: Payment date in YYYY-MM-DD format.
        
    Raises:
        ValueError: If payment is not found.
    """
    payment = get_gov_uk_dynamics_payment(id)

    if payment is None:
        raise ValueError(f"Payment not found for GOV.UK payment ID: {id}")

    dynamics_payment = get_dynamics_payment(payment.dynamics_payment_id)
    dynamics_payment.status = RECORD_STATUS_PAID
    dynamics_payment.provider_id = provider_id
    dynamics_payment.payment_date = datetime.strptime(payment_date, "%Y-%m-%d")
    db.session.commit()

    send_payment_to_mod_copying_app(dynamics_payment)
