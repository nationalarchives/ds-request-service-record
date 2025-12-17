from functools import wraps
from flask import session


def update_dynamic_back_link_mapping(*, route_key: str, back_link_value: str):
    """Update dynamic back link mappings in session."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            dynamic_back_links = session.get("dynamic_back_links", {})
            dynamic_back_links[route_key] = back_link_value
            session["dynamic_back_links"] = dynamic_back_links
            return view_func(*args, **kwargs)

        return wrapped

    return decorator
