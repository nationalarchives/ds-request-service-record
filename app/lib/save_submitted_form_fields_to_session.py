import datetime

from flask import session as flask_session
from werkzeug.datastructures import FileStorage


def save_submitted_form_fields_to_session(
    form,
    session_obj=None,
) -> None:
    """Save form field data to the session for multi-step form persistence.

    Extracts data from form fields (excluding CSRF token and submit button),
    serializes complex types like FileStorage and datetime objects, and merges
    with existing session data to maintain state across the multi-page form journey.

    Args:
        form: WTForms form instance with submitted data
        session_obj: Optional session object for testing; defaults to Flask session
    """
    # Inject a session object for easier testing. If nothing's passed, it falls back to Flask's session.
    if session_obj is None:
        session_obj = flask_session
    data = {}
    for (
        field_name,
        field,
    ) in form._fields.items():
        if field_name not in ["csrf_token", "submit"]:
            field_data = field.data

            # Normalize file uploads to a serializable value
            # We need to do this because FileStorage objects are not serializable
            if isinstance(field_data, FileStorage):
                # Store only the filename; empty string becomes 'No file uploaded'
                field_data = field_data.filename or "No file uploaded"

            if isinstance(field_data, datetime.date):
                field_data = field_data.strftime("%d %B %Y")

            if isinstance(field_data, datetime.datetime):
                field_data = field_data.date().strftime("%d %B %Y")

            data[field_name] = field_data

    # We need to merge with existing data (if any) instead of overwriting - this caught me out initially
    existing = session_obj.get("form_data")
    if isinstance(existing, dict):
        merged = existing.copy()
        merged.update(data)
        session_obj["form_data"] = merged
    else:
        session_obj["form_data"] = data
