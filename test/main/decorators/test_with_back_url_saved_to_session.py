# File: `tests/test_with_back_url_saved_to_session.py`
import pytest
from app.lib.decorators.with_back_url_saved_to_session import (
    with_route_for_back_link_saved_to_session,
)
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test-secret"

    @app.route("/first")
    @with_route_for_back_link_saved_to_session(route="main.before_you_start")
    def first():
        return "FIRST"

    @app.route("/second")
    @with_route_for_back_link_saved_to_session(
        route="main.must_submit_subject_access_request"
    )
    def second():
        return "SECOND"

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_session_key_is_set(client):
    resp = client.get("/first")
    assert resp.status_code == 200
    with client.session_transaction() as sess:
        assert sess["route_for_back_link"] == "main.before_you_start"


def test_session_key_is_overwritten(client):
    client.get("/first")
    client.get("/second")
    with client.session_transaction() as sess:
        assert sess["route_for_back_link"] == "main.must_submit_subject_access_request"


def test_decorator_requires_route():
    with pytest.raises(ValueError):

        @with_route_for_back_link_saved_to_session()  # Missing route
        def dummy():
            return "X"
