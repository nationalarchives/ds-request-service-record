import pytest
from flask import Flask, session
from app.lib.get_dynamic_back_link_route import get_dynamic_back_link_route
from app.constants import MultiPageFormRoutes


@pytest.fixture
def flask_app():
    app = Flask(__name__)
    app.secret_key = "test-secret"
    return app


def test_returns_route_when_key_exists_in_dynamic_back_links(flask_app):
    test_key = MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_CANCEL
    expected_route = MultiPageFormRoutes.BEFORE_YOU_START
    with flask_app.test_request_context("/"):
        session["dynamic_back_links"] = {test_key: expected_route}
        assert get_dynamic_back_link_route(test_key) == expected_route


def test_returns_default_route_when_key_not_found(flask_app):
    with flask_app.test_request_context("/"):
        session["dynamic_back_links"] = {"main.other_page": "main.some_route"}
        assert (
            get_dynamic_back_link_route("main.nonexistent_route")
            == MultiPageFormRoutes.JOURNEY_START.value
        )


def test_returns_default_route_when_dynamic_back_links_empty(flask_app):
    with flask_app.test_request_context("/"):
        session["dynamic_back_links"] = {}
        assert (
            get_dynamic_back_link_route("main.any_route")
            == MultiPageFormRoutes.JOURNEY_START.value
        )


def test_returns_default_route_when_session_has_no_dynamic_back_links(flask_app):
    with flask_app.test_request_context("/"):
        # Do not set session["dynamic_back_links"]
        assert (
            get_dynamic_back_link_route("main.any_route")
            == MultiPageFormRoutes.JOURNEY_START.value
        )


def test_handles_multiple_keys_in_dynamic_back_links(flask_app):
    dynamic_back_links = {
        "main.route_one": "main.another_route",
        "main.route_two": "main.yet_another_route",
        "main.route_three": "main.still_another_route",
    }
    with flask_app.test_request_context("/"):
        session["dynamic_back_links"] = dynamic_back_links
        assert get_dynamic_back_link_route("main.route_one") == "main.another_route"
        assert get_dynamic_back_link_route("main.route_two") == "main.yet_another_route"
        assert (
            get_dynamic_back_link_route("main.route_three")
            == "main.still_another_route"
        )
        assert (
            get_dynamic_back_link_route("main.route_four")
            == MultiPageFormRoutes.JOURNEY_START.value
        )
