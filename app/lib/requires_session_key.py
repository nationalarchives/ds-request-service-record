from flask import current_app, redirect, request, session, url_for


def requires_session_key(app_or_blueprint):
    @app_or_blueprint.before_request
    def check_session_key():

        required_key = "entered_through_index_page"
        exempt_routes = ["main.index", "static", "healthcheck.healthcheck"]
        short_session_id = request.cookies.get("session", "unknown")[0:7]

        # This path must be exempt because we use it to check for 308 redirects with trailing slashes
        if request.path == "/healthcheck/live":
            return

        if request.endpoint and any(
            request.endpoint.startswith(route) for route in exempt_routes
        ):
            return

        if required_key not in session or not session[required_key]:
            current_app.logger.warning(
                f"'{required_key}' not found or set on {short_session_id} session. Redirecting to start page."
            )
            return redirect(url_for("main.index"))
        else:
            current_app.logger.debug(
                f"'{required_key}' found on {short_session_id} session. Proceeding to {request.endpoint}"
            )
