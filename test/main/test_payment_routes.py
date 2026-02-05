from unittest.mock import MagicMock, patch

import pytest

from app import create_app


class DummyPayment:
    def __init__(self):
        self.id = "TEST-ID"
        self.status = "N"
        self.payee_email = "john.doe@nationalarchives.gov.uk"
        self.gov_uk_payment_id = "GOV-UK-PAY-ID"
        self.first_name = ""
        self.last_name = ""
        self.case_number = "CAS-123"
        self.net_amount = 0
        self.delivery_amount = 0
        self.total_amount = 7500
        self.details = ""
        self.reference = "PAY-0125-33-12345"


@pytest.fixture(scope="module")
def app():
    return create_app("config.Test")


@pytest.fixture()
def client(app):
    return app.test_client()


@patch("app.main.routes.dynamics_payment_routes.db")
@patch("app.main.routes.dynamics_payment_routes.send_email")
@patch("app.main.routes.dynamics_payment_routes.add_dynamics_payment")
def test_payment_creation_endpoint(
    mock_add_payment, mock_send_email, mock_db, client, app
):
    # Mock the payment creation to avoid real DB usage
    mock_add_payment.return_value = DummyPayment()
    mock_db.session.commit.return_value = None
    # Mock the query to check for existing payment - should return None for new payment
    mock_db.session.query.return_value.filter_by.return_value.first.return_value = None
    mock_send_email.return_value = True

    rv = client.post(
        f"{app.config.get('SERVICE_URL_PREFIX')}/create-payment/",
        json={
            "case_number": "CAS123",
            "net_amount": 75.00,
            "delivery_amount": 36.66,
            "reference": "PAY-0125-33-123",
            "payee_email": "john.doe@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "details": "Order of 100x A4 pages",
        },
    )
    print(rv.data)
    assert rv.status_code == 201
    data = rv.get_json()
    assert "message" in data
    assert "TEST-ID" in data["message"]


@patch("app.main.routes.dynamics_payment_routes.get_dynamics_payment")
def test_make_payment_page_renders(mock_get_payment, client, app):
    dummy = DummyPayment()
    dummy.case_number = "CAS123"
    dummy.reference = "PAY-0125-33-12345"
    dummy.net_amount = 7500
    dummy.delivery_amount = 3665
    dummy.total_amount = 11165
    dummy.first_name = "John"
    dummy.last_name = "Doe"
    dummy.details = "Order of 100x A4 pages"
    mock_get_payment.return_value = dummy

    rv = client.get(f"{app.config.get('SERVICE_URL_PREFIX')}/payment/TEST-ID/")
    assert rv.status_code == 200
    # Updated assertion to match current rendered heading
    assert dummy.case_number in rv.text
    assert dummy.reference in rv.text


@patch("app.main.routes.shared_payment_routes._fetch_payment_by_type")
def test_handle_gov_uk_pay_response_invalid_payment_type(mock_fetch, client, app):
    """Test that 400 is returned for invalid payment type."""
    with client.session_transaction() as sess:
        sess["entered_through_index_page"] = True

    rv = client.get(
        f"{app.config.get('SERVICE_URL_PREFIX')}/handle-gov-uk-pay-response/invalid_type/123/"
    )
    assert rv.status_code == 400
    mock_fetch.assert_not_called()


@patch("app.main.routes.shared_payment_routes._fetch_payment_by_type")
def test_handle_gov_uk_pay_response_payment_not_found(mock_fetch, client, app):
    """Test that 404 is returned when payment record is not found."""
    with client.session_transaction() as sess:
        sess["entered_through_index_page"] = True

    mock_fetch.return_value = None

    rv = client.get(
        f"{app.config.get('SERVICE_URL_PREFIX')}/handle-gov-uk-pay-response/dynamics/123/"
    )
    assert rv.status_code == 404
    mock_fetch.assert_called_once_with("dynamics", "123")


@patch("app.main.routes.shared_payment_routes._get_gov_uk_payment_data")
@patch("app.main.routes.shared_payment_routes._fetch_payment_by_type")
def test_handle_gov_uk_pay_response_gov_uk_pay_api_failure(
    mock_fetch, mock_get_payment_data, client, app
):
    """Test that 502 is returned when GOV.UK Pay API fails to return data."""
    with client.session_transaction() as sess:
        sess["entered_through_index_page"] = True

    dummy_payment = DummyPayment()
    mock_fetch.return_value = dummy_payment

    # Mock client with no data (API failure)
    mock_client = MagicMock()
    mock_client.data = None
    mock_get_payment_data.return_value = mock_client

    rv = client.get(
        f"{app.config.get('SERVICE_URL_PREFIX')}/handle-gov-uk-pay-response/service_record/123/"
    )
    assert rv.status_code == 502
    mock_fetch.assert_called_once_with("service_record", "123")
    mock_get_payment_data.assert_called_once_with("GOV-UK-PAY-ID")
