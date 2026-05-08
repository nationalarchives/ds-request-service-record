import pytest
from flask import url_for
from werkzeug.routing import BuildError

from app import create_app


@pytest.fixture
def app():
    return create_app("config.Test")


def test_conditionally_available_link_renders_route_href_text_and_classes(app):
    with app.test_request_context():
        macro_template = app.jinja_env.get_template(
            "macros/conditionally-available-link.html"
        )
        rendered = macro_template.module.conditionallyAvailableLink(
            "main.choose_your_order_type", "Change order", True
        )

        expected_href = url_for("main.choose_your_order_type")

    assert f'href="{expected_href}"' in rendered
    assert "Change order" in rendered


def test_conditionally_available_link_raises_for_invalid_route_name(app):
    with app.test_request_context():
        macro_template = app.jinja_env.get_template(
            "macros/conditionally-available-link.html"
        )

        with pytest.raises(BuildError):
            macro_template.module.conditionallyAvailableLink(
                "main.not_a_real_route", "Broken", True
            )


def test_conditionally_available_link_renders_nothing_when_flag_is_false(app):
    with app.test_request_context():
        macro_template = app.jinja_env.get_template(
            "macros/conditionally-available-link.html"
        )
        rendered = macro_template.module.conditionallyAvailableLink(
            "main.choose_your_order_type", "Change order", False
        )

    assert rendered.strip() == ""


def test_conditionally_available_link_renders_when_should_render_omitted(app):
    with app.test_request_context():
        macro_template = app.jinja_env.get_template(
            "macros/conditionally-available-link.html"
        )
        rendered = macro_template.module.conditionallyAvailableLink(
            "main.choose_your_order_type", "Change order"
        )

        expected_href = url_for("main.choose_your_order_type")

    assert f'href="{expected_href}"' in rendered
    assert "Change order" in rendered
