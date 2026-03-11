from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest
from app.lib.db.constants import EXPIRED_STATUS, NEW_STATUS, PAID_STATUS, SENT_STATUS
from app.lib.db.models import DynamicsPayment, db
from expire_old_payments import expire_old_payments

from app import create_app


class DummyPayment:
    def __init__(
        self,
        payment_id: str,
        email: str,
        first_name: str = "",
        last_name: str = "",
    ):
        self.id = payment_id
        self.payee_email = email
        self.first_name = first_name
        self.last_name = last_name
        self.status = "N"
        self.created_at = datetime.now(tz=timezone.utc) - timedelta(days=31)


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
    query.filter.return_value = query
    query.order_by.return_value = query
    query.all.return_value = payments


def test_expire_old_payments_updates_status_and_sends_email(context):
    payments = [
        DummyPayment("pmt-1", "one@example.com", "Jane", "Doe"),
        DummyPayment("pmt-2", "two@example.com", "", ""),
    ]

    with (
        patch("expire_old_payments.db") as mock_db,
        patch("expire_old_payments.send_email", return_value=True) as mock_send_email,
    ):
        _mock_query_chain(mock_db, payments)

        expired_count = expire_old_payments(days=30)

    assert expired_count == 2
    assert payments[0].status == EXPIRED_STATUS
    assert payments[1].status == EXPIRED_STATUS
    assert mock_db.session.commit.call_count == 2
    assert mock_send_email.call_count == 2


def test_expire_old_payments_logs_when_email_fails(context):
    payment = DummyPayment("pmt-3", "three@example.com")

    with (
        patch("expire_old_payments.db") as mock_db,
        patch("expire_old_payments.send_email", return_value=False),
        patch("expire_old_payments.current_app.logger.error") as mock_log_error,
    ):
        _mock_query_chain(mock_db, [payment])

        expired_count = expire_old_payments(days=30)

    assert expired_count == 1
    assert payment.status == EXPIRED_STATUS
    assert mock_db.session.commit.call_count == 1
    mock_log_error.assert_called_once()


def test_expire_old_payments_rolls_back_on_commit_error(context):
    payment = DummyPayment("pmt-4", "four@example.com")

    with (
        patch("expire_old_payments.db") as mock_db,
        patch("expire_old_payments.send_email", return_value=True),
        patch("expire_old_payments.current_app.logger.error") as mock_log_error,
    ):
        _mock_query_chain(mock_db, [payment])
        mock_db.session.commit.side_effect = Exception("db commit failed")

        expired_count = expire_old_payments(days=30)

    assert expired_count == 0
    assert mock_db.session.rollback.call_count == 1
    mock_log_error.assert_called_once()


def test_expire_old_payments_uses_30_day_cutoff_and_only_new_status(db_session):
    fixed_now = datetime(2026, 3, 11, 0, 0, 0, tzinfo=timezone.utc)

    payment_31_days = DynamicsPayment(
        id="pmt-31-days-new",
        case_number="CASE-31",
        reference="REF-31",
        net_amount=1000,
        delivery_amount=0,
        total_amount=1000,
        payee_email="older-than-30@example.com",
        status=NEW_STATUS,
        created_at=fixed_now - timedelta(days=31),
    )
    payment_30_days = DynamicsPayment(
        id="pmt-30-days-new",
        case_number="CASE-30",
        reference="REF-30",
        net_amount=1000,
        delivery_amount=0,
        total_amount=1000,
        payee_email="exactly-30@example.com",
        status=NEW_STATUS,
        created_at=fixed_now - timedelta(days=30),
    )
    payment_29_days = DynamicsPayment(
        id="pmt-29-days-new",
        case_number="CASE-29",
        reference="REF-29",
        net_amount=1000,
        delivery_amount=0,
        total_amount=1000,
        payee_email="newer-than-30@example.com",
        status=NEW_STATUS,
        created_at=fixed_now - timedelta(days=29),
    )
    payment_paid_31_days = DynamicsPayment(
        id="pmt-31-days-paid",
        case_number="CASE-31-PAID",
        reference="REF-31-PAID",
        net_amount=1000,
        delivery_amount=0,
        total_amount=1000,
        payee_email="paid@example.com",
        status=PAID_STATUS,
        created_at=fixed_now - timedelta(days=31),
    )
    payment_sent_31_days = DynamicsPayment(
        id="pmt-31-days-sent",
        case_number="CASE-31-SENT",
        reference="REF-31-SENT",
        net_amount=1000,
        delivery_amount=0,
        total_amount=1000,
        payee_email="sent@example.com",
        status=SENT_STATUS,
        created_at=fixed_now - timedelta(days=31),
    )

    db_session.add_all(
        [
            payment_31_days,
            payment_30_days,
            payment_29_days,
            payment_paid_31_days,
            payment_sent_31_days,
        ]
    )
    db_session.commit()

    with (
        patch("expire_old_payments.datetime") as mock_datetime,
        patch("expire_old_payments.send_email", return_value=True) as mock_send_email,
    ):
        mock_datetime.now.return_value = fixed_now
        expired_count = expire_old_payments(days=30)

    assert expired_count == 1

    p31_new = db_session.get(DynamicsPayment, "pmt-31-days-new")
    p30_new = db_session.get(DynamicsPayment, "pmt-30-days-new")
    p29_new = db_session.get(DynamicsPayment, "pmt-29-days-new")
    p31_paid = db_session.get(DynamicsPayment, "pmt-31-days-paid")
    p31_sent = db_session.get(DynamicsPayment, "pmt-31-days-sent")

    assert p31_new.status == EXPIRED_STATUS
    assert p30_new.status == NEW_STATUS
    assert p29_new.status == NEW_STATUS
    assert p31_paid.status == PAID_STATUS
    assert p31_sent.status == SENT_STATUS
    mock_send_email.assert_called_once()
