"""Helpers for reading and normalising a service person's date of birth.

The application stores DOBs in the session as human-readable strings such as
"01 January 1926". This module converts that session representation into a real
`date` object so the rest of the application can compare years reliably, use
boundary checks, and decide whether proof-of-death requirements apply.
"""

from datetime import date

from flask import session as flask_session

# The session stores DOBs in a readable format like "01 January 1926". We map
# each month name to its numeric value so we can build a real Python date object
# for calculations and comparisons elsewhere in the app.
MONTH_NAME_TO_NUMBER = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}


def parse_date_of_birth(date_of_birth: str) -> date:
    """Parse a DOB stored in session format into a Python `date`.

    This is intentionally strict: the app expects inputs in the format produced by
    the form and the session, so a malformed value should fail early rather than
    silently producing a bad date.
    """
    try:
        day_str, month_str, year_str = date_of_birth.split(" ", 2)
        day = int(day_str)
        year = int(year_str)
        month = MONTH_NAME_TO_NUMBER[month_str]
        return date(year, month, day)
    except Exception as exc:
        raise ValueError(f"Invalid date of birth: {date_of_birth!r}") from exc


def get_date_of_birth_from_session(session_obj=None) -> date | None:
    """Retrieve a DOB from session['form_data'] and normalise it to a `date`.

    This keeps session access in one place. Callers can ask for the DOB once and
    then rely on a clean `date` object for year comparisons and rule decisions.
    """
    if session_obj is None:
        session_obj = flask_session

    try:
        date_of_birth = session_obj["form_data"]["date_of_birth"]
    except (KeyError, TypeError):
        return None

    if not date_of_birth:
        return None

    return parse_date_of_birth(date_of_birth)
