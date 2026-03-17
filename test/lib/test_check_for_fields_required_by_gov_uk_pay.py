import pytest

from app.lib.check_for_fields_required_by_gov_uk_pay import (
    check_for_fields_required_by_gov_uk_pay,
)


class DummyLogger:
    def __init__(self):
        self.warnings = []

    def warning(self, msg, *args):
        self.warnings.append((msg, args))


class DummyApp:
    def __init__(self):
        self.logger = DummyLogger()


@pytest.fixture
def app():
    return DummyApp()


@pytest.fixture
def valid_serviceperson_data():
    return {
        "forenames": "Test",
        "last_name": "Test",
        "date_of_birth": "1900-01-01",
    }


@pytest.fixture
def valid_postal_data():
    return {
        "requester_address1": "1 Nonexistent Street",
        "requester_town_city": "London",
        "requester_postcode": "XX11 1XX",
        "requester_country": "United Kingdom",
    }


def test_returns_true_when_serviceperson_and_email_present(
    app, valid_serviceperson_data
):
    form_data = {
        **valid_serviceperson_data,
        "requester_email": "test@example.com",
    }

    assert check_for_fields_required_by_gov_uk_pay(form_data, app) is True
    assert app.logger.warnings == []


def test_returns_true_when_serviceperson_and_all_postal_present(
    app, valid_serviceperson_data, valid_postal_data
):
    form_data = {
        **valid_serviceperson_data,
        **valid_postal_data,
    }

    assert check_for_fields_required_by_gov_uk_pay(form_data, app) is True
    assert app.logger.warnings == []


def test_returns_true_when_serviceperson_email_and_postal_present(
    app, valid_serviceperson_data, valid_postal_data
):
    form_data = {
        **valid_serviceperson_data,
        **valid_postal_data,
        "requester_email": "test@example.com",
    }

    assert check_for_fields_required_by_gov_uk_pay(form_data, app) is True
    assert app.logger.warnings == []


@pytest.mark.parametrize("missing_field", ["forenames", "last_name", "date_of_birth"])
def test_returns_false_when_required_serviceperson_field_missing(
    app, valid_serviceperson_data, missing_field
):
    form_data = dict(valid_serviceperson_data)
    form_data.pop(missing_field)
    form_data["requester_email"] = "test@example.com"

    assert check_for_fields_required_by_gov_uk_pay(form_data, app) is False
    assert len(app.logger.warnings) == 1
    msg, args = app.logger.warnings[0]
    assert "missing the required field" in msg
    assert args == (missing_field,)


def test_returns_false_when_no_email_and_incomplete_postal(
    app, valid_serviceperson_data, valid_postal_data
):
    form_data = {
        **valid_serviceperson_data,
        **valid_postal_data,
    }
    form_data.pop("requester_postcode")

    assert check_for_fields_required_by_gov_uk_pay(form_data, app) is False
    assert len(app.logger.warnings) == 1
    msg, args = app.logger.warnings[0]
    assert "missing requester_email or incomplete postal address fields" in msg
    assert args == ()


def test_returns_false_when_no_email_and_no_postal(app, valid_serviceperson_data):
    form_data = dict(valid_serviceperson_data)

    assert check_for_fields_required_by_gov_uk_pay(form_data, app) is False
    assert len(app.logger.warnings) == 1
    msg, args = app.logger.warnings[0]
    assert "missing requester_email or incomplete postal address fields" in msg
    assert args == ()


def test_empty_email_treated_as_missing_with_complete_postal_is_true(
    app, valid_serviceperson_data, valid_postal_data
):
    form_data = {
        **valid_serviceperson_data,
        **valid_postal_data,
        "requester_email": "",
    }

    assert check_for_fields_required_by_gov_uk_pay(form_data, app) is True
    assert app.logger.warnings == []
