import pytest
from flask import Flask, request
from flask import session as flask_session
from app.lib.save_catalogue_reference_to_session import save_catalogue_reference_to_session


def make_app():
    app = Flask(__name__)
    app.secret_key = "test-secret"
    return app


def test_saves_catalogue_reference_into_empty_session():
    app = make_app()
    session_obj = {}
    with app.test_request_context("/x?catalogue_reference=WO", method="GET"):
        save_catalogue_reference_to_session(request, session_obj=session_obj)
    assert session_obj["form_data"] == {"catalogue_reference": "WO"}


def test_ignores_when_method_not_get():
    app = make_app()
    session_obj = {}
    with app.test_request_context("/x?catalogue_reference=WO 95", method="POST"):
        save_catalogue_reference_to_session(request, session_obj=session_obj)
    assert session_obj.get("form_data") == {} # session["form_data"] is empty


def test_ignores_when_param_missing():
    app = make_app()
    session_obj = {}
    with app.test_request_context("/x", method="GET"):
        save_catalogue_reference_to_session(request, session_obj=session_obj)
    assert session_obj.get("form_data") == {}  # session["form_data"] is empty


def test_ignores_empty_string_value():
    app = make_app()
    session_obj = {}
    with app.test_request_context("/x?catalogue_reference=", method="GET"):
        save_catalogue_reference_to_session(request, session_obj=session_obj)
    assert session_obj.get("form_data") == {} # session["form_data"] is empty


def test_merges_with_existing_preserving_other_keys():
    app = make_app()
    session_obj = {"form_data": {"something_else": "x"}}
    with app.test_request_context("/x?catalogue_reference=WO 1234", method="GET"):
        save_catalogue_reference_to_session(request, session_obj=session_obj)
    assert session_obj["form_data"] == {"something_else": "x", "catalogue_reference": "WO 1234"}


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("<script>alert(document.cookie)</script>", "&lt;script&gt;alert(document.cookie)&lt;/script&gt;"),
        ("<iframe src='' onmouseover='alert(document.cookie)'></iframe>","&lt;iframe src=&#39;&#39; onmouseover=&#39;alert(document.cookie)&#39;&gt;&lt;/iframe&gt;"),
        ("<a href='javascript:alert(String.fromCharCode(88,83,83))'>Click Me!</a>","&lt;a href=&#39;javascript:alert(String.fromCharCode(88,83,83))&#39;&gt;Click Me!&lt;/a&gt;"),
        ("WO 123", "WO 123"),
    ],
)
def test_escaping_applied_to_value(raw, expected):
    app = make_app()
    session_obj = {}
    with app.test_request_context(f"/x?catalogue_reference={raw}", method="GET"):
        save_catalogue_reference_to_session(request, session_obj=session_obj)
    assert session_obj["form_data"]["catalogue_reference"] == expected


def test_fallback_to_flask_session_when_no_session_obj():
    app = make_app()
    with app.test_request_context("/x?catalogue_reference=WO", method="GET"):
        save_catalogue_reference_to_session(request)  # We're not passing session_obj
        assert flask_session["form_data"] == {"catalogue_reference": "WO"}


def test_no_change_to_existing_when_no_new_field():
    app = make_app()
    session_obj = {"form_data": {"something_else": "x"}}
    with app.test_request_context("/x", method="GET"):
        save_catalogue_reference_to_session(request, session_obj=session_obj)
    assert session_obj["form_data"] == {"something_else": "x"}
