# python
import pytest
from flask import Flask, session
from app.lib.decorators.update_dynamic_back_link_mapping import (
    update_dynamic_back_link_mapping,
)
from app.constants import MultiPageFormRoutes


@pytest.fixture
def flask_app():
    """Create a Flask app for testing."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test-secret-key"
    return app


class TestUpdateDynamicBackLinkMapping:
    """Test suite for the update_dynamic_back_link_mapping decorator."""

    def test_adds_mapping_to_empty_session(self, flask_app):
        """Should create new dynamic_back_links when session is empty."""
        with flask_app.test_request_context():

            @update_dynamic_back_link_mapping(
                mappings={
                    MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_CANCEL: MultiPageFormRoutes.BEFORE_YOU_START
                }
            )
            def view():
                return "success"

            view()

            assert session["dynamic_back_links"] == {
                MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_CANCEL: MultiPageFormRoutes.BEFORE_YOU_START
            }

    def test_adds_mapping_to_existing_session(self, flask_app):
        """Should add to existing dynamic_back_links."""
        with flask_app.test_request_context():
            session["dynamic_back_links"] = {
                "main.some_other_route": "main.another_route"
            }

            @update_dynamic_back_link_mapping(
                mappings={
                    MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_CANCEL: MultiPageFormRoutes.BEFORE_YOU_START
                }
            )
            def view():
                return "success"

            view()

            assert session["dynamic_back_links"] == {
                "main.some_other_route": "main.another_route",
                MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_CANCEL: MultiPageFormRoutes.BEFORE_YOU_START,
            }

    def test_overwrites_existing_route_key(self, flask_app):
        """Should overwrite existing route key with new value."""
        with flask_app.test_request_context():
            session["dynamic_back_links"] = {
                MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_CANCEL: "main.old_route_value"
            }

            @update_dynamic_back_link_mapping(
                mappings={
                    MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_CANCEL: "main.new_route_value"
                }
            )
            def view():
                return "success"

            view()

            assert session["dynamic_back_links"] == {
                MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_CANCEL: "main.new_route_value"
            }

    def test_passes_arguments_to_view(self, flask_app):
        """Should pass all arguments through to decorated view."""
        with flask_app.test_request_context():

            @update_dynamic_back_link_mapping(mappings={"test": "/test"})
            def view(*args, **kwargs):
                return {"args": args, "kwargs": kwargs}

            result = view("arg1", "arg2", key="value")

            assert result == {"args": ("arg1", "arg2"), "kwargs": {"key": "value"}}

    def test_propagates_exceptions(self, flask_app):
        """Should propagate exceptions from decorated view."""
        with flask_app.test_request_context():

            @update_dynamic_back_link_mapping(mappings={"test": "/test"})
            def view():
                raise ValueError("Test error")

            with pytest.raises(ValueError, match="Test error"):
                view()

    def test_requires_keyword_arguments(self):
        """Should require keyword-only arguments."""
        with pytest.raises(TypeError):
            update_dynamic_back_link_mapping({"route": "/back"})

    def test_preserves_other_session_data(self, flask_app):
        """Should not affect other session data."""
        with flask_app.test_request_context():
            session["user_id"] = 123
            session["preferences"] = {"theme": "dark"}

            @update_dynamic_back_link_mapping(mappings={"test": "/test"})
            def view():
                return "success"

            view()

            assert session["user_id"] == 123
            assert session["preferences"] == {"theme": "dark"}
            assert session["dynamic_back_links"] == {"test": "/test"}

    def test_adds_multiple_mappings(self, flask_app):
        """Should add multiple key/value pairs at once."""
        with flask_app.test_request_context():

            @update_dynamic_back_link_mapping(
                mappings={
                    "a": "/a",
                    "b": "/b",
                }
            )
            def view():
                return "success"

            view()

            assert session["dynamic_back_links"] == {"a": "/a", "b": "/b"}
