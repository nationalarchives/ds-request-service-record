import pytest
from flask import Flask, session
from app.lib.decorators.with_form_prefilled_from_session import with_form_prefilled_from_session

class MockForm:
    def __init__(self, data=None):
        self.data = data or {}

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test"

    @app.route("/test", methods=["GET", "POST"])
    @with_form_prefilled_from_session(MockForm)
    def test_view(form):
        return form.data or "empty"

    return app

def test_get_prefills_form_from_session(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["foo"] = "bar"
            sess["csrf_token"] = "should be ignored"
        response = client.get("/test")
        assert b"foo" in response.data
        assert b"bar" in response.data
        assert b"csrf_token" not in response.data

def test_post_does_not_prefill_form(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["foo"] = "bar"
        response = client.post("/test")
        assert b"foo" not in response.data