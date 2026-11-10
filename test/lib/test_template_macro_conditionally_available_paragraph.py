from app import create_app


def test_conditionally_available_paragraph_renders_content_when_should_render_is_true():
    app = create_app("config.Test")
    macro_template = app.jinja_env.get_template(
        "macros/conditionally-available-paragraph.html"
    )

    rendered = macro_template.module.conditionallyAvailableParagraph(
        "This should be rendered", True
    )

    assert "<p>This should be rendered</p>" in rendered
    assert "data-testid" not in rendered


def test_conditionally_available_paragraph_renders_test_id_when_provided():
    app = create_app("config.Test")
    macro_template = app.jinja_env.get_template(
        "macros/conditionally-available-paragraph.html"
    )

    rendered = macro_template.module.conditionallyAvailableParagraph(
        "This should be rendered", True, testId="test-paragraph"
    )

    assert '<p data-testid="test-paragraph">This should be rendered</p>' in rendered


def test_conditionally_available_paragraph_renders_nothing_when_should_render_is_false():
    app = create_app("config.Test")
    macro_template = app.jinja_env.get_template(
        "macros/conditionally-available-paragraph.html"
    )

    rendered = macro_template.module.conditionallyAvailableParagraph(
        "This should not be rendered", False
    )

    assert rendered.strip() == ""
