import pytest
from flask import Flask, session as flask_session

from app.lib.save_submitted_form_fields_to_session import (
    save_submitted_form_fields_to_session,
)


class DummyField:
    def __init__(self, data):
        self.data = data


class DummyForm:
    def __init__(self, **fields):
        # Mimic WTForms' internal _fields mapping
        self._fields = {name: DummyField(value) for name, value in fields.items()}


def test_saves_basic_fields_into_empty_session():
    session_obj = {}
    form = DummyForm(
        first_name="Francis",
        last_name="Palgrave",
        csrf_token="ignore",
        submit="ignored",
    )
    # Add csrf_token & submit explicitly so we can verify they are ignored
    form._fields["csrf_token"] = DummyField("TOKEN")
    form._fields["submit"] = DummyField("Submit")

    save_submitted_form_fields_to_session(form, session_obj=session_obj)

    assert "form_data" in session_obj
    assert session_obj["form_data"] == {
        "first_name": "Francis",
        "last_name": "Palgrave",
    }


def test_merges_with_existing_dict_overwriting_new_values():
    session_obj = {
        "form_data": {"first_name": "Thomas", "middle_name": "Duffus", "age": 272}
    }
    form = DummyForm(first_name="William", last_name="Hardy")

    save_submitted_form_fields_to_session(form, session_obj=session_obj)

    assert session_obj["form_data"] == {
        "first_name": "William",  # overwritten
        "middle_name": "Duffus",  # preserved
        "age": 272,  # preserved
        "last_name": "Hardy",  # added
    }


def test_replaces_non_dict_existing_data():
    session_obj = {"form_data": ["not", "a", "dict"]}
    form = DummyForm(field1="value1")

    save_submitted_form_fields_to_session(form, session_obj=session_obj)

    assert session_obj["form_data"] == {"field1": "value1"}


def test_ignores_csrf_and_submit_fields():
    session_obj = {}
    form = DummyForm(csrf_token="abc", submit="Send", real_field="value")
    # Ensure keys exist exactly with those names
    save_submitted_form_fields_to_session(form, session_obj=session_obj)
    assert session_obj["form_data"] == {"real_field": "value"}
    assert "csrf_token" not in session_obj["form_data"]
    assert "submit" not in session_obj["form_data"]


def test_empty_payload_does_not_modify_existing_when_no_new_fields():
    session_obj = {"form_data": {"already": 1}}
    form = DummyForm()  # no fields at all
    save_submitted_form_fields_to_session(form, session_obj=session_obj)
    # Should be unchanged
    assert session_obj["form_data"] == {"already": 1}


def test_fallback_to_flask_session_when_no_session_obj_passed():
    app = Flask(__name__)
    app.secret_key = "test-secret"  # Needed for session

    form = DummyForm(city="London", country="UK")

    with app.test_request_context():
        save_submitted_form_fields_to_session(
            form
        )  # no session_obj -> uses flask's session
        assert flask_session["form_data"] == {"city": "London", "country": "UK"}


# Edge case: overlapping but empty new value should still overwrite
@pytest.mark.parametrize(
    "existing,new_value,expected",
    [
        ("Thomas", "", ""),
        ("Thomas", None, None),
    ],
)
def test_overwrite_with_falsey_values(existing, new_value, expected):
    session_obj = {"form_data": {"field": existing, "other": 123}}
    form = DummyForm(field=new_value)
    save_submitted_form_fields_to_session(form, session_obj=session_obj)
    assert session_obj["form_data"] == {"field": expected, "other": 123}
