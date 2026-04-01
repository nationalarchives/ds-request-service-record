"""
Command to run to resend paid Dynamics payments to the MOD Copying API.

This is intended to be run as a cron job, to ensure that
any second payments that were marked as PAID but failed to
send to the MOD Copying API are retried.
"""

import os

from app.lib.db.constants import PAID_STATUS, SENT_STATUS
from app.lib.db.models import DynamicsPayment, db
from app.lib.dynamics_handler import send_payment_to_mod_copying_app
from flask import current_app

from app import create_app


def resend_paid_dynamics_payments() -> int:
    paid_payments = (
        db.session.query(DynamicsPayment)
        .filter_by(status=PAID_STATUS)
        .order_by(DynamicsPayment.created_at)
        .all()
    )

    sent_count = 0
    for payment in paid_payments:
        try:
            if send_payment_to_mod_copying_app(payment):
                payment.status = SENT_STATUS
                db.session.commit()
                sent_count += 1
            else:
                db.session.rollback()
        except Exception as exc:
            db.session.rollback()
            current_app.logger.error(
                "Error resending paid dynamics payment %s: %s", payment.id, exc
            )

    return sent_count


def main() -> None:
    app = create_app(os.getenv("CONFIG", "config.Production"))
    with app.app_context():
        sent_count = resend_paid_dynamics_payments()
        app.logger.info("Resent %s PAID status dynamics payments", sent_count)


if __name__ == "__main__":
    main()
