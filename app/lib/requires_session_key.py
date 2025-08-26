from flask import current_app, redirect, request, session, url_for


def requires_session_key(app_or_blueprint):
    @app_or_blueprint.before_request
    def check_session_key():

        required_key = "entered_through_index_page"

        exempt_routes = [
            "main.index",
            "main.start",
            "static",
            "healthcheck.healthcheck",
            "main.gov_uk_pay_webhook",
        ]

        short_session_id = request.cookies.get("session", "unknown")[0:7]

        # This path must be exempt because we use it to check for 308 redirects with trailing slashes
        if request.path == "/healthcheck/live":
            return

        if request.endpoint and any(
            request.endpoint.startswith(route) for route in exempt_routes
        ):
            # If the route is exempt, we set the session key to True
            session["entered_through_index_page"] = True
            return

        if required_key not in session or not session[required_key]:
            current_app.logger.warning(
                f"'{required_key}' not found or set on {short_session_id} session. Redirecting to start page."
            )
            # If the session key is not set, we set the session key to True before redirecting
            session["entered_through_index_page"] = True
            return redirect(url_for("main.index"))
