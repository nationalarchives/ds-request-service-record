"""Session management utilities"""

from flask import current_app, redirect, request, session, url_for


def invalidate_existing_session():
    """Invalidate the existing session and redirect to the start if it belongs to an older journey version."""

    excluded_endpoints = {
        "healthcheck.healthcheck",
        "static",
    }

    if request.endpoint in excluded_endpoints:
        return

    # Get the current session invalidation version from the app config
    current_version = current_app.config["SESSION_INVALIDATION_VERSION"]

    # Get the session invalidation version from the current session
    session_version = session.get("_session_invalidation_version")

    # No existing journey session, set the current version in the session
    if session_version is None:
        session["_session_invalidation_version"] = current_version
        return

    # Existing session belongs to an older journey version
    if session_version != current_version:
        session.clear()
        session["_session_invalidation_version"] = current_version
        redirect(url_for("main.start"))

    return
