# python
from enum import Enum
from functools import wraps
from flask import session


def update_dynamic_back_link_mapping(*, mappings: dict[Enum, Enum]):
    """Update dynamic back link mappings in session with provided dictionary."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            dynamic_back_links = session.get("dynamic_back_links", {})
            # Merge provided mappings, overwriting existing keys
            dynamic_back_links.update(mappings)
            session["dynamic_back_links"] = dynamic_back_links
            return view_func(*args, **kwargs)

        return wrapped

    return decorator
