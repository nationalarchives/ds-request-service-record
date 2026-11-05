import pytest

from app import create_app


@pytest.fixture
def app():
    return create_app("config.Test")


def test_conditionally_available_warning_renders_when_should_render_is_true(app):
    with app.test_request_context():
        macro_template = app.jinja_env.get_template(
            "macros/conditionally-available-warning.html"
        )
        rendered = macro_template.module.conditionallyAvailableWarning(
            {
                "message": "This warning should be rendered",
                "heading_level": 3,
                "should_render": True,
            }
        )

    assert "This warning should be rendered" in rendered


def test_conditionally_available_warning_renders_nothing_when_flag_is_false(app):
    with app.test_request_context():
        macro_template = app.jinja_env.get_template(
            "macros/conditionally-available-warning.html"
        )
        rendered = macro_template.module.conditionallyAvailableWarning(
            {
                "message": "This warning should not be rendered",
                "heading_level": 3,
                "should_render": False,
            }
        )

    assert rendered.strip() == ""


def test_conditionally_available_warning_renders_nothing_when_should_render_is_omitted(
    app,
):
    with app.test_request_context():
        macro_template = app.jinja_env.get_template(
            "macros/conditionally-available-warning.html"
        )
        rendered = macro_template.module.conditionallyAvailableWarning(
            {
                "message": "This warning should not be rendered",
                "heading_level": 3,
            }
        )

    assert rendered.strip() == ""


def test_conditionally_available_warning_uses_requested_heading_level(app):
    with app.test_request_context():
        macro_template = app.jinja_env.get_template(
            "macros/conditionally-available-warning.html"
        )
        rendered = macro_template.module.conditionallyAvailableWarning(
            {
                "message": "This warning should render with an h4 heading",
                "heading_level": 4,
                "should_render": True,
            }
        )

    assert '<h4 class="tna-warning__heading">' in rendered
