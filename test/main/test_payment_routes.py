from unittest.mock import patch

import pytest

from app import create_app


class DummyPayment:
    def __init__(self):
        self.id = "TEST-ID"
        self.status = "N"
        self.payee_email = "john.doe@nationalarchives.gov.uk"


@pytest.fixture(scope="module")
def app():
    return create_app("config.Test")


@pytest.fixture()
def client(app):
    return app.test_client()


@patch("app.main.routes.payment_routes.db")
@patch("app.main.routes.payment_routes.send_email")
@patch("app.main.routes.payment_routes.add_dynamics_payment")
def test_payment_creation_endpoint(mock_add_payment, mock_send_email, mock_db, client):
    # Mock the payment creation to avoid real DB usage
    mock_add_payment.return_value = DummyPayment()
    mock_db.session.commit.return_value = None
    mock_send_email.return_value = True

    rv = client.post(
        "/request-a-military-service-record/create-payment/",
        json={
            "case_number": "CAS123",
            "net_amount": 75.00,
            "delivery_amount": 36.66,
            "reference": "PAY-0125-33-123/4325",
            "payee_email": "john.doe@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "details": "Order of 100x A4 pages",
        },
    )

    assert rv.status_code == 201
    data = rv.get_json()
    assert "message" in data
    assert "TEST-ID" in data["message"]


@patch("app.main.routes.payment_routes.get_dynamics_payment")
def test_make_payment_page_renders(mock_get_payment, client):
    dummy = DummyPayment()
    dummy.case_number = "CAS123"
    dummy.reference = "PAY-0125-33-123/4325"
    dummy.net_amount = 7500
    dummy.delivery_amount = 3665
    dummy.total_amount = 11165
    dummy.first_name = "John"
    dummy.last_name = "Doe"
    dummy.details = "Order of 100x A4 pages"
    mock_get_payment.return_value = dummy

    rv = client.get("/request-a-military-service-record/payment/TEST-ID/")
    assert rv.status_code == 200
    # Updated assertion to match current rendered heading
    assert dummy.case_number in rv.text
    assert dummy.reference in rv.text
