from functools import wraps

from flask import session, request

"""
This decorator allows us to persist a back-link route in the Flask session.
We need this because there are some pages that can be reached from multiple
parts of the app and we want to ensure their 'Back' link always goes to the
page the user was last on.

Provides:
    with_endpoint_saved_to_journey_history() decorator

Usage example:
    @with_endpoint_saved_to_journey_history
    def dashboard():
        ...
"""


def with_endpoint_saved_to_journey_history(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        print(request.endpoint)
        history = session.get("journey_history", [])
        if not history or history[-1] != request.endpoint:
            history.append(request.endpoint)
            session["journey_history"] = history
        return view_func(*args, **kwargs)

    return wrapped
