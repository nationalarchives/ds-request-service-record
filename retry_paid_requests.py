"""
Command to run to resend paid requests to Dynamics.

This is intended to be run as a cron job, to ensure that
any requests that were marked as PAID but failed to send
to Dynamics are retried.
"""

import os

from app.lib.db.constants import PAID_STATUS, SENT_STATUS
from app.lib.db.models import ServiceRecordRequest, db
from app.lib.dynamics_handler import send_request_to_dynamics
from flask import current_app

from app import create_app


def resend_paid_requests() -> int:
    paid_requests = (
        db.session.query(ServiceRecordRequest)
        .filter_by(status=PAID_STATUS)
        .order_by(ServiceRecordRequest.created_at)
        .all()
    )

    sent_count = 0
    for record in paid_requests:
        try:
            if send_request_to_dynamics(record):
                record.status = SENT_STATUS
                db.session.commit()
                sent_count += 1
            else:
                db.session.rollback()
        except Exception as exc:
            db.session.rollback()
            current_app.logger.error(
                "Error resending service record request %s: %s", record.id, exc
            )

    return sent_count


def main() -> None:
    app = create_app(os.getenv("CONFIG", "config.Production"))
    with app.app_context():
        sent_count = resend_paid_requests()
        app.logger.info("Resent %s PAID status requests", sent_count)


if __name__ == "__main__":
    main()
