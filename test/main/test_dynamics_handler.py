from datetime import UTC, datetime
from unittest.mock import MagicMock, patch
from xml.etree import ElementTree

import pytest
import requests

from app import create_app
from app.lib.db.models import DynamicsPayment, ServiceRecordRequest
from app.lib.dynamics_handler import (
    generate_tagged_request,
    send_payment_to_mod_copying_app,
    subject_status,
)


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
    recent_year = datetime.now(UTC).year - 40
    dob = f"15 June {recent_year}"
    r = DummyRecord(dob, "file.png", "standard")
    assert subject_status(r) == "? FOI DIRECT MOD FOICD1"


def test_no_evidence_sets_FOICDN_standard(context):
    recent_year = datetime.now(UTC).year - 30
    dob = f"10 March {recent_year}"
    r = DummyRecord(dob, None, "standard")
    assert subject_status(r) == "? FOI DIRECT MOD FOICDN1"


def test_no_evidence_sets_FOICDN_full(context):
    recent_year = datetime.now(UTC).year - 25
    dob = f"20 August {recent_year}"
    r = DummyRecord(dob, None, "full")
    assert subject_status(r) == "? FOI DIRECT MOD FOICDN2"


def test_generate_tagged_request_includes_commissioned_officer_status(context):
    record = ServiceRecordRequest(
        requester_first_name="Jane",
        requester_last_name="Doe",
        requester_email="jane@example.com",
        requester_address1="1 Test Street",
        requester_town_city="London",
        requester_country="United Kingdom",
        forenames="John",
        last_name="Smith",
        date_of_birth="01 January 1950",
        were_they_a_commissioned_officer="unknown",
    )

    tagged_request = generate_tagged_request(record)

    assert "<commissioned_officer>unknown</commissioned_officer>" in tagged_request


@pytest.mark.parametrize(
    ("attribute", "tag"),
    [
        ("requester_first_name", "mandatory_forename"),
        ("additional_information", "enquiry"),
        ("proof_of_death", "mandatory_upload_file_name"),
    ],
)
@pytest.mark.parametrize(
    "value",
    [
        "Smith & Jones",
        '<injected attribute="value">text</injected>',
        "</enquiry><injected>text</injected><enquiry>",
        "<![CDATA[text]]>",
        '&lt;already escaped&gt; "quoted" \'text\'',
    ],
)
def test_generate_tagged_request_escapes_xml_values(context, attribute, tag, value):
    record = ServiceRecordRequest(
        date_of_birth=f"01 January {datetime.now(UTC).year - 40}",
        **{attribute: value},
    )

    tagged_request = generate_tagged_request(record)
    root = ElementTree.fromstring(f"<request>{tagged_request}</request>")
    element = root.find(tag)

    assert element is not None
    assert element.text == value
    assert len(element) == 0
    assert root.find("injected") is None


@pytest.mark.parametrize(
    ("date_of_birth", "proof_of_death", "expected"),
    [
        ("01 January 1900", None, "Not applicable"),
        ("01 January 1900", "<file>.png", "Not applicable"),
        (f"01 January {datetime.now(UTC).year - 40}", None, None),
        (f"01 January {datetime.now(UTC).year - 40}", "EMPTY", None),
    ],
)
def test_generate_tagged_request_preserves_upload_placeholder(
    context, date_of_birth, proof_of_death, expected
):
    record = ServiceRecordRequest(
        date_of_birth=date_of_birth, proof_of_death=proof_of_death
    )

    tagged_request = generate_tagged_request(record)
    root = ElementTree.fromstring(f"<request>{tagged_request}</request>")

    assert root.findtext("mandatory_upload_file_name") == expected


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
        payment_date=datetime(2024, 3, 15, 14, 30, 0, tzinfo=UTC),
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
def test_send_payment_to_mod_copying_app_returns_false_on_error(mock_post, context):
    """Test that the function returns False when API returns non-200 status"""
    # Setup mock response with error
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("HTTP 500")
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
        payment_date=datetime(2024, 3, 15, 14, 30, 0, tzinfo=UTC),
    )

    # Verify it returns False on error
    assert send_payment_to_mod_copying_app(payment) is False
