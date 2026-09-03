from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app import create_app
from app.lib.db.constants import NEW_STATUS, PAID_STATUS, SENT_STATUS
from app.lib.db.models import DynamicsPayment, db
from retry_paid_dynamics_payments import resend_paid_dynamics_payments


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


def test_resend_paid_dynamics_payments_updates_sent_status(db_session):
    payments = [
        DynamicsPayment(
            id=f"pmt-{index}",
            case_number=f"CASE-{index}",
            reference=f"REF-{index}",
            net_amount=1000,
            delivery_amount=200,
            total_amount=1200,
            payee_email=f"payment-{index}@example.com",
            status=PAID_STATUS,
        )
        for index in (1, 2)
    ]
    db_session.add_all(payments)
    db_session.commit()

    with patch(
        "retry_paid_dynamics_payments.send_payment_to_mod_copying_app",
        return_value=True,
    ):
        sent_count = resend_paid_dynamics_payments()

    assert sent_count == 2
    assert all(
        db_session.get(DynamicsPayment, payment.id).status == SENT_STATUS
        for payment in payments
    )


def test_resend_paid_dynamics_payments_rolls_back_when_send_fails(db_session):
    payment = DynamicsPayment(
        id="pmt-3",
        case_number="CASE-3",
        reference="REF-3",
        net_amount=1000,
        delivery_amount=200,
        total_amount=1200,
        payee_email="payment-3@example.com",
        status=PAID_STATUS,
    )
    db_session.add(payment)
    db_session.commit()

    with patch(
        "retry_paid_dynamics_payments.send_payment_to_mod_copying_app",
        return_value=False,
    ):
        sent_count = resend_paid_dynamics_payments()

    assert sent_count == 0
    assert db_session.get(DynamicsPayment, payment.id).status == PAID_STATUS


def test_resend_paid_dynamics_payments_rolls_back_on_exception(db_session):
    payment = DynamicsPayment(
        id="pmt-4",
        case_number="CASE-4",
        reference="REF-4",
        net_amount=1000,
        delivery_amount=200,
        total_amount=1200,
        payee_email="payment@example.com",
        status=PAID_STATUS,
    )
    db_session.add(payment)
    db_session.commit()

    with (
        patch(
            "retry_paid_dynamics_payments.send_payment_to_mod_copying_app",
            return_value=True,
        ),
        patch("retry_paid_dynamics_payments.current_app.logger.error") as mock_error,
        patch.object(
            db_session, "commit", side_effect=SQLAlchemyError("db commit failed")
        ),
    ):
        sent_count = resend_paid_dynamics_payments()

    assert sent_count == 0
    assert payment.status == PAID_STATUS
    assert db_session.get(DynamicsPayment, "pmt-4").status == PAID_STATUS
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
