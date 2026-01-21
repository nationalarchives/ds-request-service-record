"""
This module sets up a background scheduler that periodically sends GET requests
to the MOD Copying API endpoint. This is neeeded to keep the connection active,
preventing timeouts during periods of inactivity.

While this is not an ideal solution, it is a necessary workaround due to limitations
in the MOD Copying API infrastructure - ideally, the API server would not timeout in
periods of inactivity on production.
"""

import logging
import os
from datetime import datetime

import requests
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)


def send_get_request():
    """
    Send a GET request to an external endpoint.
    """
    # Get the endpoint URL from environment variable or config
    endpoint_url = (
        os.environ.get(
            "RECORD_COPYING_SERVICE_API_URL", "https://example.com/api/health"
        )
        + "GetCountry"
    )

    try:
        response = requests.get(endpoint_url, timeout=10)
        if response.status_code in [200, 201, 202]:
            logger.info(
                f"GET request successful at {datetime.now()}: {endpoint_url} - Status: {response.status_code}"
            )
        else:
            logger.warning(
                f"GET request returned status {response.status_code} at {datetime.now()}: {endpoint_url}"
            )
    except requests.exceptions.RequestException as e:
        logger.error(f"GET request failed at {datetime.now()}: {str(e)}")


def init_scheduler(app):
    """
    Initialize the scheduler with the Flask app.
    Only runs in the first worker process to avoid duplicate jobs.

    Args:
        app: Flask application instance
    """
    # Only start scheduler in one worker to avoid duplicate jobs
    # Check if we're in a Gunicorn worker by looking at environment variables
    import sys

    # In Gunicorn, only start scheduler in the first worker
    # The WERKZEUG_RUN_MAIN check prevents duplicate schedulers in Flask dev mode
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or "gunicorn" not in sys.argv[0]:
        # Check worker ID (gunicorn sets different process IDs)
        worker_id = os.getpid()

        # Use a lock file to ensure only one scheduler starts
        lock_file = "/tmp/scheduler.lock"

        if not os.path.exists(lock_file):
            try:
                # Create lock file
                with open(lock_file, "w") as f:
                    f.write(str(worker_id))

                scheduler = BackgroundScheduler()

                # Schedule the GET request task to run every 10 minutes
                scheduler.add_job(
                    func=send_get_request,
                    trigger="interval",
                    seconds=600,
                    id="get_request_job",
                    name="Send GET request every 10 minutes",
                    replace_existing=True,
                )

                # Start the scheduler
                scheduler.start()
                logger.info(
                    f"Scheduler started in process {worker_id} - GET requests will be sent every 30 seconds"
                )

                # Shut down the scheduler and remove lock file when the app stops
                import atexit

                def cleanup():
                    scheduler.shutdown()
                    if os.path.exists(lock_file):
                        os.remove(lock_file)

                atexit.register(cleanup)

                return scheduler
            except Exception as e:
                logger.error(f"Failed to start scheduler: {e}")
        else:
            logger.info(
                f"Scheduler already running in another worker (PID: {worker_id})"
            )
    else:
        logger.info("Skipping scheduler initialization in reloader process")

    return None
