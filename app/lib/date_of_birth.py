from datetime import date

from flask import session as flask_session

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
    """Parse a DOB string in the session format into a date object."""
    try:
        day_str, month_str, year_str = date_of_birth.split(" ", 2)
        day = int(day_str)
        year = int(year_str)
        month = MONTH_NAME_TO_NUMBER[month_str]
        return date(year, month, day)
    except Exception as exc:
        raise ValueError(f"Invalid date of birth: {date_of_birth!r}") from exc


def get_date_of_birth_from_session(session_obj=None) -> date | None:
    """Get and parse date_of_birth from session['form_data']."""
    if session_obj is None:
        session_obj = flask_session

    try:
        date_of_birth = session_obj["form_data"]["date_of_birth"]
    except (KeyError, TypeError):
        return None

    if not date_of_birth:
        return None

    return parse_date_of_birth(date_of_birth)
