from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from app.lib.db.constants import NEW_STATUS, PAID_STATUS, SENT_STATUS
from app.lib.db.models import DynamicsPayment, db
from retry_paid_dynamics_payments import resend_paid_dynamics_payments

from app import create_app


class DummyPayment:
    def __init__(self, payment_id: str, status: str = PAID_STATUS):
        self.id = payment_id
        self.status = status
        self.created_at = datetime.now(tz=timezone.utc)


@pytest.fixture(scope="module")
def app():
    return create_app("config.Test")


@pytest.fixture()
def context(app):
    with app.app_context():
        yield


@pytest.fixture()
def db_session(app):
    with app.app_context():
        db.create_all()
        db.session.query(DynamicsPayment).delete()
        db.session.commit()
        yield db.session
        db.session.query(DynamicsPayment).delete()
        db.session.commit()


def _mock_query_chain(mock_db, payments):
    query = MagicMock()
    mock_db.session.query.return_value = query
    query.filter_by.return_value = query
    query.order_by.return_value = query
    query.all.return_value = payments


def test_resend_paid_dynamics_payments_updates_sent_status(context):
    payments = [DummyPayment("pmt-1"), DummyPayment("pmt-2")]

    with (
        patch("retry_paid_dynamics_payments.db") as mock_db,
        patch(
            "retry_paid_dynamics_payments.send_payment_to_mod_copying_app",
            return_value=True,
        ),
    ):
        _mock_query_chain(mock_db, payments)

        sent_count = resend_paid_dynamics_payments()

    assert sent_count == 2
    assert payments[0].status == SENT_STATUS
    assert payments[1].status == SENT_STATUS
    assert mock_db.session.commit.call_count == 2


def test_resend_paid_dynamics_payments_rolls_back_when_send_fails(context):
    payment = DummyPayment("pmt-3")

    with (
        patch("retry_paid_dynamics_payments.db") as mock_db,
        patch(
            "retry_paid_dynamics_payments.send_payment_to_mod_copying_app",
            return_value=False,
        ),
    ):
        _mock_query_chain(mock_db, [payment])

        sent_count = resend_paid_dynamics_payments()

    assert sent_count == 0
    assert payment.status == PAID_STATUS
    assert mock_db.session.rollback.call_count == 1


def test_resend_paid_dynamics_payments_rolls_back_on_exception(context):
    payment = DummyPayment("pmt-4")

    with (
        patch("retry_paid_dynamics_payments.db") as mock_db,
        patch(
            "retry_paid_dynamics_payments.send_payment_to_mod_copying_app",
            side_effect=Exception("HTTP 500"),
        ),
        patch("retry_paid_dynamics_payments.current_app.logger.error") as mock_error,
    ):
        _mock_query_chain(mock_db, [payment])

        sent_count = resend_paid_dynamics_payments()

    assert sent_count == 0
    assert payment.status == PAID_STATUS
    assert mock_db.session.rollback.call_count == 1
    mock_error.assert_called_once()


def test_resend_paid_dynamics_payments_only_retries_paid_status(db_session):
    paid_payment = DynamicsPayment(
        id="pmt-paid",
        case_number="CASE-PAID",
        reference="REF-PAID",
        net_amount=1000,
        delivery_amount=200,
        total_amount=1200,
        payee_email="paid@example.com",
        status=PAID_STATUS,
    )
    new_payment = DynamicsPayment(
        id="pmt-new",
        case_number="CASE-NEW",
        reference="REF-NEW",
        net_amount=1000,
        delivery_amount=200,
        total_amount=1200,
        payee_email="new@example.com",
        status=NEW_STATUS,
    )
    sent_payment = DynamicsPayment(
        id="pmt-sent",
        case_number="CASE-SENT",
        reference="REF-SENT",
        net_amount=1000,
        delivery_amount=200,
        total_amount=1200,
        payee_email="sent@example.com",
        status=SENT_STATUS,
    )

    db_session.add_all([paid_payment, new_payment, sent_payment])
    db_session.commit()

    with patch(
        "retry_paid_dynamics_payments.send_payment_to_mod_copying_app",
        return_value=True,
    ) as mock_send:
        sent_count = resend_paid_dynamics_payments()

    assert sent_count == 1
    assert db_session.get(DynamicsPayment, "pmt-paid").status == SENT_STATUS
    assert db_session.get(DynamicsPayment, "pmt-new").status == NEW_STATUS
    assert db_session.get(DynamicsPayment, "pmt-sent").status == SENT_STATUS
    mock_send.assert_called_once()
