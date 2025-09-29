from functools import wraps

from flask import request, session


def with_form_prefilled_from_session(form_class):
    excluded_form_data_fields = ["what_was_their_date_of_birth"]

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            if request.method == "GET":
                form_data = session.get("form_data", {})
                if not isinstance(form_data, dict):
                    form_data = {}
                data = {k: v for k, v in form_data.items() if k not in excluded_form_data_fields}
                form = form_class(data=data)
            else:
                form = form_class()
            return view_func(form, *args, **kwargs)

        return wrapped

    return decorator
