from flask import current_app, redirect, request, session, url_for


def requires_session_key():
    required_key = "entered_through_index_page"

    exempt_routes = [
        "main.start",
        "main.create_payment_endpoint",
        "main.make_payment",
        "main.sorry_you_will_have_to_start_again",
        "main.handle_gov_uk_pay_response",
        "main.request_submitted",
    ]

    if request.endpoint and any(
        request.endpoint.startswith(route) for route in exempt_routes
    ):
        # If the route is exempt, we set the session key to True
        session["entered_through_index_page"] = True
        return None

    if required_key not in session or not session[required_key]:
        current_app.logger.info(
            f"'{required_key}' not found or set in session. Redirecting to start page."
        )
        # If the session key is not set, we set the session key to True before redirecting
        session["entered_through_index_page"] = True
        return redirect(url_for("main.start"))

    return None
