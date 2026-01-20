import datetime

from app.lib.save_submitted_form_fields_to_session import (
    save_submitted_form_fields_to_session,
)
from werkzeug.datastructures import FileStorage


class MockField:
    def __init__(self, data):
        self.data = data


class MockForm:
    def __init__(self, fields):
        # fields: dict of field_name -> MockField
        self._fields = fields


def test_serializes_filestorage_filename():
    session_obj = {}
    fs = FileStorage(stream=None, filename="proof-of-death.png")
    form = MockForm(
        {
            "csrf_token": MockField("secret"),
            "submit": MockField("Submit"),
            "file_field": MockField(fs),
        }
    )

    save_submitted_form_fields_to_session(form, session_obj=session_obj)

    assert session_obj["form_data"]["file_field"] == "proof-of-death.png"
    assert "csrf_token" not in session_obj["form_data"]
    assert "submit" not in session_obj["form_data"]


def test_serializes_filestorage_empty_filename_to_placeholder():
    session_obj = {}
    fs = FileStorage(stream=None, filename="")
    form = MockForm({"file_field": MockField(fs)})

    save_submitted_form_fields_to_session(form, session_obj=session_obj)

    assert session_obj["form_data"]["file_field"] == "No file uploaded"


def test_formats_date_and_datetime():
    session_obj = {}
    d = datetime.date(2024, 7, 5)  # 05 July 2024
    dt = datetime.datetime(2023, 12, 31, 23, 59)  # 31 December 2023
    form = MockForm(
        {
            "date_field": MockField(d),
            "datetime_field": MockField(dt),
            "text_field": MockField("hello"),
        }
    )

    save_submitted_form_fields_to_session(form, session_obj=session_obj)

    assert session_obj["form_data"]["date_field"] == "05 July 2024"
    assert session_obj["form_data"]["datetime_field"] == "31 December 2023"
    assert session_obj["form_data"]["text_field"] == "hello"


def test_merges_with_existing_form_data_dict():
    session_obj = {"form_data": {"existing": "keep", "to_override": "old"}}
    form = MockForm(
        {
            "to_override": MockField("new"),
            "added": MockField(123),
        }
    )

    save_submitted_form_fields_to_session(form, session_obj=session_obj)

    assert session_obj["form_data"] == {
        "existing": "keep",
        "to_override": "new",
        "added": 123,
    }


def test_overwrites_when_existing_is_not_dict():
    session_obj = {"form_data": ["not", "a", "dict"]}
    form = MockForm({"a": MockField(1)})

    save_submitted_form_fields_to_session(form, session_obj=session_obj)

    assert session_obj["form_data"] == {"a": 1}
