import pytest
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
    # WireMock returns £4.50 = 450 pence
    assert fee == 450


def test_calculate_delivery_fee_us(app_context):
    """Test delivery fee calculation for US."""
    fee = calculate_delivery_fee("United States")
    # WireMock returns £11.00 = 1100 pence
    assert fee == 1100


def test_calculate_delivery_fee_other_country(app_context):
    """Test delivery fee calculation for other countries."""
    fee = calculate_delivery_fee("France")
    # WireMock returns £8.50 = 850 pence
    assert fee == 850


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
    assert amount == 5166


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


def test_prepare_order_summary_data(app_context):
    """Test order summary data preparation."""
    form_data = {
        "processing_option": "standard",
        "does_not_have_email": False,
    }

    summary = prepare_order_summary_data(form_data)

    assert summary["processing_option"] == "standard"
    assert summary["delivery_type"] == "Digital"
    assert summary["amount_pence"] == 4225
