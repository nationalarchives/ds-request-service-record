from unittest.mock import patch

import pytest
import requests

from app import create_app
from app.lib.order_summary_data import prepare_order_summary_data


@pytest.fixture
def app(wiremock_server):
    """Create and configure a test app instance."""
    app = create_app("config.Test")
    return app


@pytest.fixture
def app_context(app):
    """Provide an application context for tests."""
    with app.app_context():
        yield app


def test_prepare_order_summary_data_standard_digital(app_context):
    """Test order summary data preparation for standard digital delivery."""
    form_data = {
        "processing_option": "standard",
        "does_not_have_email": False,
    }

    summary = prepare_order_summary_data(form_data)

    assert summary["processing_option"] == "standard"
    assert summary["delivery_type"] == "Digital"
    assert summary["amount_pence"] == 4225
    assert summary["delivery_fee_pence"] == 0
    assert summary["order_type"] == "standard_digital"


def test_prepare_order_summary_data_standard_printed(app_context):
    """Test order summary data preparation for printed delivery."""
    form_data = {
        "processing_option": "standard",
        "does_not_have_email": True,
        "requester_country": "United Kingdom",
    }

    summary = prepare_order_summary_data(form_data)

    assert summary["processing_option"] == "standard"
    assert summary["delivery_type"] == "PrintedTracked"
    assert summary["amount_pence"] == 4716
    assert summary["delivery_fee_pence"] == 795
    assert summary["order_type"] == "standard_printed"


def test_prepare_order_summary_data_full_record_check_printed(app_context):
    """Test order summary data preparation for full record check printed delivery."""
    form_data = {
        "processing_option": "full",
        "does_not_have_email": True,
        "requester_country": "United Kingdom",
    }

    summary = prepare_order_summary_data(form_data)

    assert summary["processing_option"] == "full"
    assert summary["delivery_type"] == "PrintedTracked"
    assert summary["amount_pence"] == 4887
    assert summary["delivery_fee_pence"] == 0
    assert summary["order_type"] == "full_record_check_printed"


def test_prepare_order_summary_data_full_record_check_digital(app_context):
    """Test order summary data preparation for full record check digital delivery."""
    form_data = {
        "processing_option": "full",
        "does_not_have_email": False,
    }

    summary = prepare_order_summary_data(form_data)

    assert summary["processing_option"] == "full"
    assert summary["delivery_type"] == "Digital"
    assert summary["amount_pence"] == 4887
    assert summary["delivery_fee_pence"] == 0
    assert summary["order_type"] == "full_record_check_digital"


@pytest.mark.parametrize(
    "service_branch,commissioned_officer, does_not_have_email, expected_order_type",
    [
        (
            "BRITISH_ARMY",
            "yes",
            True,
            "full_record_check_printed",
        ),
        (
            "BRITISH_ARMY",
            "yes",
            False,
            "full_record_check_digital",
        ),
    ],
)
def test_prepare_order_summary_data_with_service_branch_and_commissioned_officer(
    app_context,
    service_branch,
    commissioned_officer,
    does_not_have_email,
    expected_order_type,
):
    """Test order summary data preparation for full record check digital delivery."""
    form_data = {
        "processing_option": "full",
        "does_not_have_email": does_not_have_email,
        "were_they_a_commissioned_officer": commissioned_officer,
        "service_branch": service_branch,
    }

    summary = prepare_order_summary_data(form_data)

    assert summary["service_branch"] == service_branch
    assert summary["were_they_a_commissioned_officer"] == commissioned_officer
    assert summary["order_type"] == expected_order_type


def test_prepare_order_summary_data_when_form_data_is_none(app_context):
    """Test order summary preparation returns None when form data is missing."""
    result = prepare_order_summary_data(None)

    assert result is None


def test_prepare_order_summary_data_when_api_fails(app_context):
    """Test order summary preparation when delivery fee API fails."""
    form_data = {
        "processing_option": "standard",
        "does_not_have_email": True,
        "requester_country": "United Kingdom",
    }

    with patch("app.lib.price_calculations.requests.post") as mock_post:
        mock_post.side_effect = requests.exceptions.HTTPError("500 Server Error")

        result = prepare_order_summary_data(form_data)

        # Should return None when API fails
        assert result is None
