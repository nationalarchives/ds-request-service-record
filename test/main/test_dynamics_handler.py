from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from app.lib.db.models import DynamicsPayment
from app.lib.dynamics_handler import send_payment_to_mod_copying_app, subject_status

from app import create_app


class DummyRecord:
    def __init__(self, date_of_birth, proof_of_death, processing_option):
        self.date_of_birth = date_of_birth
        self.proof_of_death = proof_of_death
        self.processing_option = processing_option


@pytest.fixture(scope="module")
def app():
    return create_app("config.Test")


@pytest.fixture()
def context(app):
    with app.app_context():
        yield


def test_age_over_115_sets_FOIOP(context):
    dob = "01 January 1900"
    r = DummyRecord(dob, None, "standard")
    assert subject_status(r) == "? FOI DIRECT MOD FOIOP1"


def test_proof_of_death_sets_FOICD(context):
    recent_year = datetime.now().year - 40
    dob = f"15 June {recent_year}"
    r = DummyRecord(dob, "file.png", "standard")
    assert subject_status(r) == "? FOI DIRECT MOD FOICD1"


def test_no_evidence_sets_FOICDN_standard(context):
    recent_year = datetime.now().year - 30
    dob = f"10 March {recent_year}"
    r = DummyRecord(dob, None, "standard")
    assert subject_status(r) == "? FOI DIRECT MOD FOICDN1"


def test_no_evidence_sets_FOICDN_full(context):
    recent_year = datetime.now().year - 25
    dob = f"20 August {recent_year}"
    r = DummyRecord(dob, None, "full")
    assert subject_status(r) == "? FOI DIRECT MOD FOICDN2"


@patch("app.lib.dynamics_handler.requests.post")
def test_send_payment_to_mod_copying_app_payload_format(mock_post, context):
    """Test that the payload sent to MOD Copying API maintains the expected format"""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Create test payment
    payment = DynamicsPayment(
        id="test-payment-id",
        case_number="CASE123",
        reference="PAY-REF-456",
        provider_id="gov-uk-pay-id-789",
        total_amount=15000,  # Amount in pence (£150.00)
        net_amount=12000,
        delivery_amount=3000,
        payee_email="test@example.com",
        payment_date=datetime(2024, 3, 15, 14, 30, 0),
    )

    # Call the function
    send_payment_to_mod_copying_app(payment)

    # Verify requests.post was called once
    assert mock_post.call_count == 1

    # Extract the call arguments
    call_args = mock_post.call_args

    # Verify the expected payload structure and format
    expected_payload = {
        "CaseNumber": "CASE123",
        "PayReference": "PAY-REF-456",
        "GovUkProviderId": "gov-uk-pay-id-789",
        "Amount": 150.0,  # Divided by 100
        "Date": "2024-03-15 14:30:00",
    }

    # Assertions on the payload
    actual_payload = call_args.kwargs["json"]
    assert actual_payload == expected_payload


@patch("app.lib.dynamics_handler.requests.post")
def test_send_payment_to_mod_copying_app_raises_on_error(mock_post, context):
    """Test that the function raises ValueError when API returns non-200 status"""
    # Setup mock response with error
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_post.return_value = mock_response

    # Create test payment
    payment = DynamicsPayment(
        id="test-payment-id",
        case_number="CASE123",
        reference="PAY-REF-456",
        provider_id="gov-uk-pay-id-789",
        total_amount=15000,
        net_amount=12000,
        delivery_amount=3000,
        payee_email="test@example.com",
        payment_date=datetime(2024, 3, 15, 14, 30, 0),
    )

    # Verify it raises ValueError
    with pytest.raises(ValueError, match="Could not update MOD Copying app"):
        send_payment_to_mod_copying_app(payment)
