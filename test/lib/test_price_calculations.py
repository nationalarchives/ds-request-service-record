from unittest.mock import patch

import pytest
import requests
from app.lib.price_calculations import (
    calculate_amount_based_on_form_data,
    calculate_delivery_fee,
    get_delivery_type,
    prepare_order_summary_data,
)

from app import create_app


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


def test_calculate_delivery_fee_uk(app_context):
    """Test delivery fee calculation for UK."""
    fee = calculate_delivery_fee("United Kingdom")
    # WireMock returns £7.95 = 795 pence
    assert fee == 795


def test_calculate_delivery_fee_us(app_context):
    """Test delivery fee calculation for US."""
    fee = calculate_delivery_fee("United States")
    # WireMock returns £20.31 = 2031 pence
    assert fee == 2031


def test_calculate_delivery_fee_other_country(app_context):
    """Test delivery fee calculation for other countries."""
    fee = calculate_delivery_fee("France")
    # WireMock returns £12.61 = 1261 pence
    assert fee == 1261


def test_get_delivery_type_digital():
    """Test delivery type is digital when email is provided."""
    form_data = {"does_not_have_email": False}
    assert get_delivery_type(form_data) == "Digital"


def test_get_delivery_type_printed():
    """Test delivery type is printed when no email."""
    form_data = {"does_not_have_email": True}
    assert get_delivery_type(form_data) == "PrintedTracked"


def test_calculate_amount_standard_digital(app_context):
    """Test amount calculation for standard digital delivery."""
    form_data = {
        "processing_option": "standard",
        "does_not_have_email": False,
    }
    amount = calculate_amount_based_on_form_data(form_data)
    assert amount == 4225


def test_calculate_amount_full_digital(app_context):
    """Test amount calculation for full digital delivery."""
    form_data = {
        "processing_option": "full",
        "does_not_have_email": False,
    }
    amount = calculate_amount_based_on_form_data(form_data)
    assert amount == 4887


def test_calculate_amount_standard_printed_with_delivery(app_context):
    """Test amount calculation for standard printed with delivery fee."""
    form_data = {
        "processing_option": "standard",
        "does_not_have_email": True,
        "requester_country": "United Kingdom",
    }
    amount = calculate_amount_based_on_form_data(form_data)
    assert amount == 5511


def test_calculate_amount_full_printed(app_context):
    """Test amount calculation for full printed delivery."""
    form_data = {
        "processing_option": "full",
        "does_not_have_email": True,
        "requester_country": "United Kingdom",
    }
    amount = calculate_amount_based_on_form_data(form_data)
    assert amount == 4887


def test_calculate_amount_invalid_processing_option(app_context):
    """Test error handling for invalid processing option."""
    form_data = {
        "processing_option": "invalid",
        "does_not_have_email": False,
    }
    with pytest.raises(ValueError, match="Invalid processing option"):
        calculate_amount_based_on_form_data(form_data)


def test_calculate_amount_printed_without_country(app_context):
    """Test error handling when country is missing for printed delivery."""
    form_data = {
        "processing_option": "standard",
        "does_not_have_email": True,
    }
    with pytest.raises(ValueError, match="Country is required for printed delivery"):
        calculate_amount_based_on_form_data(form_data)


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


def test_calculate_delivery_fee_api_error(app_context):
    """Test delivery fee calculation when API returns an error."""
    with patch("app.lib.price_calculations.requests.post") as mock_post:
        mock_post.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("500 Server Error")
        )

        with pytest.raises(requests.exceptions.HTTPError):
            calculate_delivery_fee("United Kingdom")


def test_calculate_delivery_fee_api_timeout(app_context):
    """Test delivery fee calculation when API times out."""
    with patch("app.lib.price_calculations.requests.post") as mock_post:
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")

        with pytest.raises(requests.exceptions.Timeout):
            calculate_delivery_fee("United Kingdom")


def test_calculate_delivery_fee_api_connection_error(app_context):
    """Test delivery fee calculation when API is unreachable."""
    with patch("app.lib.price_calculations.requests.post") as mock_post:
        mock_post.side_effect = requests.exceptions.ConnectionError("Failed to connect")

        with pytest.raises(requests.exceptions.ConnectionError):
            calculate_delivery_fee("United Kingdom")


def test_calculate_delivery_fee_invalid_json_response(app_context):
    """Test delivery fee calculation when API returns invalid JSON."""
    with patch("app.lib.price_calculations.requests.post") as mock_post:
        mock_response = mock_post.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("Invalid JSON")

        with pytest.raises(ValueError):
            calculate_delivery_fee("United Kingdom")


def test_calculate_amount_when_delivery_fee_api_fails(app_context):
    """Test amount calculation when delivery fee API fails for printed delivery."""
    form_data = {
        "processing_option": "standard",
        "does_not_have_email": True,
        "requester_country": "United Kingdom",
    }

    with patch("app.lib.price_calculations.requests.post") as mock_post:
        mock_post.side_effect = requests.exceptions.HTTPError("500 Server Error")

        with pytest.raises(requests.exceptions.HTTPError):
            calculate_amount_based_on_form_data(form_data)


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
