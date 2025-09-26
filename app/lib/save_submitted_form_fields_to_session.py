from flask import session as flask_session


def save_submitted_form_fields_to_session(
    form,
    session_obj=None,
) -> None:
    # I'm injecting a session object for easier testing. If nothing's passed, it falls back to Flask's session.
    if session_obj is None:
        session_obj = flask_session
    data = {}
    for (
        field_name,
        field,
    ) in form._fields.items():
        if field_name not in ["csrf_token", "submit"]:
            data[field_name] = field.data
    # We need to merge with existing data (if any) instead of overwriting - this caught me out initially
    existing = session_obj.get("form_data")
    if isinstance(existing, dict):
        merged = existing.copy()
        merged.update(data)
        session_obj["form_data"] = merged
    else:
        session_obj["form_data"] = data
