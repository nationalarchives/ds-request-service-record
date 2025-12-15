import pytest
from flask import Flask
from app.lib.decorators.with_endpoint_saved_to_journey_history import with_endpoint_saved_to_journey_history

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test_secret"

    @app.route("/test1")
    @with_endpoint_saved_to_journey_history
    def test1():
        return "test1"

    @app.route("/test2")
    @with_endpoint_saved_to_journey_history
    def test2():
        return "test2"

    return app

def test_journey_history_stores_endpoint(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["journey_history"] = []

        response = client.get("/test1")
        assert response.data == b"test1"
        with client.session_transaction() as sess:
            assert sess["journey_history"] == ["test1"]

def test_journey_history_appends_new_endpoint(app):
    with app.test_client() as client:
        client.get("/test1")
        client.get("/test2")
        with client.session_transaction() as sess:
            assert sess["journey_history"] == ["test1", "test2"]

def test_journey_history_does_not_duplicate_endpoint(app):
    with app.test_client() as client:
        client.get("/test1")
        client.get("/test1")
        with client.session_transaction() as sess:
            assert sess["journey_history"] == ["test1"]
