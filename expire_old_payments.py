"""
Command to expire Dynamics payments older than 30 days.

This is intended to be run as a cron job.
"""

import os
from datetime import datetime, timedelta, timezone

from app import create_app
from app.lib.aws import send_email
from app.lib.db.constants import EXPIRED_STATUS, NEW_STATUS
from app.lib.db.models import DynamicsPayment, db
from flask import current_app


def expire_old_payments(days: int = 30) -> int:
    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=days)

    payments = (
        db.session.query(DynamicsPayment)
        .filter(DynamicsPayment.status == NEW_STATUS)
        .filter(DynamicsPayment.created_at < cutoff)
        .order_by(DynamicsPayment.created_at)
        .all()
    )

    expired_count = 0
    for payment in payments:
        try:
            payment.status = EXPIRED_STATUS
            db.session.commit()
            expired_count += 1
            name = (
                f"{payment.first_name or ''} {payment.last_name or ''}".strip()
                or "customer"
            )
            if not send_email(
                to=payment.payee_email,
                subject="Your payment link has expired",
                body=(
                    f"Dear {name},\n\n"
                    "Your payment link for your service record request has expired. "
                    "Please contact us if you still need to make this payment.\n\n"
                    "Thank you,\n"
                    "Request a military service record team\n"
                    "The National Archives"
                ),
            ):
                current_app.logger.error(
                    "Failed to send expiry email for dynamics payment %s",
                    payment.id,
                )
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                "Error expiring dynamics payment %s: %s", payment.id, e
            )

    return expired_count


def main() -> None:
    app = create_app(os.getenv("CONFIG", "config.Production"))
    with app.app_context():
        expired_count = expire_old_payments()
        app.logger.info("Expired %s Dynamics payments", expired_count)


if __name__ == "__main__":
    main()
