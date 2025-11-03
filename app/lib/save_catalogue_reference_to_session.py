from flask import session as flask_session
from markupsafe import escape


def save_catalogue_reference_to_session(
    request,
    session_obj=None,
) -> None:
    # Session object is injected for easier testing. If nothing's passed, it falls back to Flask's session.
    if session_obj is None:
        session_obj = flask_session
    data = {}
    if request.method == "GET" and request.args.get("catalogue_reference"):
        safe_catalogue_reference = escape(
            request.args.get("catalogue_reference", "")
        )
        data["catalogue_reference"] = str(safe_catalogue_reference)

    # We need to merge with existing data (if any) instead of overwriting - this caught me out initially
    existing = session_obj.get("form_data")
    if isinstance(existing, dict):
        merged = existing.copy()
        merged.update(data)
        session_obj["form_data"] = merged
    else:
        session_obj["form_data"] = data
