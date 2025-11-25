from functools import wraps
from flask import request, session, url_for

"""
This decorator allows us to persist a back-link route in the Flask session.
We need this because there are some pages that can be reached from multiple
parts of the app and we want to ensure their 'Back' link always go to the 
correct page.

Provides:
    with_route_for_back_link_saved_to_session(route)
        Before the wrapped view runs, stores the given endpoint name under
        session["route_for_back_link"] so templates or later logic can build
        a consistent Back link (e.g., url_for(session["route_for_back_link"])).
        
        This only needs to be added to specific 'gateway' views which once entered
        indicate where the user should go back to from subsequent pages. 

Usage example:
    @with_route_for_back_link_saved_to_session(MultiPageFormRoutes.BEFORE_YOU_START.value)
    def dashboard():
        ...

Notes:
- The stored value is overwritten on every decorated call, which is the intended behaviour.
- Store endpoint names, not full URLs.
"""


def with_route_for_back_link_saved_to_session(*, route: str | None = None):
    if route is None:
        raise ValueError("Route is required")

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            session["route_for_back_link"] = route
            return view_func(*args, **kwargs)

        return wrapped

    return decorator
