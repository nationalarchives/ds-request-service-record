from datetime import date

import pytest

from app import create_app
from app.lib.date_of_birth import get_date_of_birth_from_session, parse_date_of_birth


@pytest.fixture()
def app_context():
    app = create_app("config.Test")
    with app.test_request_context():
        yield


def test_parse_date_of_birth_returns_date():
    assert parse_date_of_birth("01 January 1926") == date(1926, 1, 1)


@pytest.mark.parametrize("value", ["", "not a date", "32 January 1926"])
def test_parse_date_of_birth_raises_value_error_for_invalid_values(value):
    with pytest.raises(ValueError):
        parse_date_of_birth(value)


def test_get_date_of_birth_from_session_returns_none_when_missing(app_context):
    assert get_date_of_birth_from_session() is None


def test_get_date_of_birth_from_session_parses_value(app_context):
    from flask import session

    session["form_data"] = {"date_of_birth": "01 January 1926"}

    assert get_date_of_birth_from_session() == date(1926, 1, 1)


def test_get_date_of_birth_from_session_raises_value_error_for_malformed_value(
    app_context,
):
    from flask import session

    session["form_data"] = {"date_of_birth": "not a real date"}

    with pytest.raises(ValueError):
        get_date_of_birth_from_session()
