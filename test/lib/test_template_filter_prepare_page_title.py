from jinja2 import Environment
from types import SimpleNamespace

from app.lib.template_filters import prepare_page_title


def render_with_filter(template_str, context):
    env = Environment()
    env.filters["prepare_page_title"] = prepare_page_title
    tmpl = env.from_string(template_str)
    return tmpl.render(context)


class FakeAppObj:
    def __init__(self, title=None):
        self.title = title


# If there is no form and no context, we should not error and just return the title as is.
def test_page_title_no_form_no_context():
    tpl = "{{ 'Before you start' | prepare_page_title }}"
    out = render_with_filter(tpl, {})
    assert out == "Before you start"


# If there are no errors on the form, we should not add the 'Error: ' prefix.
def test_page_title_form_without_errors_attr():
    tpl = "{{ 'Before you start' | prepare_page_title }}"
    ctx = {"form": object()}  # no 'errors' attribute
    out = render_with_filter(tpl, ctx)
    assert out == "Before you start"


# If errors has fields, we should add the "Error: " prefix
def test_page_title_with_errors_prefix_added():
    tpl = "{{ 'Before you start' | prepare_page_title }}"
    ctx = {"form": SimpleNamespace(errors={"field": ["sad times"]})}
    out = render_with_filter(tpl, ctx)
    assert out == "Error: Before you start"


# If errors exists but is empty, we should not add the prefix.
def test_page_title_no_errors_no_prefix():
    tpl = "{{ 'Before you start' | prepare_page_title }}"
    ctx = {"form": SimpleNamespace(errors={})}
    out = render_with_filter(tpl, ctx)
    assert out == "Before you start"


# Where there is a title, it's included with the separator.
def test_page_title_content_dict_app_title_added():
    tpl = "{{ 'Before you start' | prepare_page_title }}"
    ctx = {"content": {"app": {"title": "Request a military service record"}}}
    out = render_with_filter(tpl, ctx)
    assert out == "Before you start - Request a military service record"


# Where there is a title and errors, they're returned correctly.
def test_page_title_errors_and_app_title():
    tpl = "{{ 'Before you start' | prepare_page_title }}"
    ctx = {
        "form": SimpleNamespace(errors={"field": ["sad times"]}),
        "content": {"app": {"title": "Request a military service record"}},
    }
    out = render_with_filter(tpl, ctx)
    assert out == "Error: Before you start - Request a military service record"


# If the app property is missing from `content`, we just return the original string.
def test_page_title_missing_app_in_dict():
    tpl = "{{ 'Before you start' | prepare_page_title }}"
    ctx = {"content": {}}
    out = render_with_filter(tpl, ctx)
    assert out == "Before you start"


# If the title property is missing from `app`, we just return the original string.
def test_page_title_missing_app_title_in_dict():
    tpl = "{{ 'Before you start' | prepare_page_title }}"
    ctx = {"content": {"app": {}}}
    out = render_with_filter(tpl, ctx)
    assert out == "Before you start"


# None should be an empty string
def test_page_title_title_none_becomes_empty_string():
    tpl = "{{ None | prepare_page_title }}"
    out = render_with_filter(tpl, {})
    assert out == ""


# An empty string with an app title should return just the app title.
def test_page_title_title_empty_string_with_app_title():
    tpl = "{{ '' | prepare_page_title }}"
    ctx = {"content": {"app": {"title": "Request a military service record"}}}
    out = render_with_filter(tpl, ctx)
    assert out == "Request a military service record"


# If we have an error and an app title, but the string is empty,
# we should return just the app title with the error prefix.
def test_page_title_title_empty_string_with_errors_and_app_title():
    tpl = "{{ '' | prepare_page_title }}"
    ctx = {
        "form": SimpleNamespace(errors={"field": ["sad times"]}),
        "content": {"app": {"title": "Request a military service record"}},
    }
    out = render_with_filter(tpl, ctx)
    assert out == "Error: Request a military service record"


# Whitespace around the input string should be stripped from the result.
def test_page_title_strips_whitespace_in_result():
    tpl = "{{ '  Before you start  ' | prepare_page_title }}"
    ctx = {
        "form": SimpleNamespace(errors={}),
        "content": {"app": {"title": "Request a military service record"}},
    }
    out = render_with_filter(tpl, ctx)
    # Function only trims overall string; internal spaces in 'title' remain
    assert out == "Before you start - Request a military service record"


# Non strings are coerced for inclusion
def test_page_title_non_string_title_is_coerced():
    tpl = "{{ 123 | prepare_page_title }}"
    out = render_with_filter(tpl, {})
    assert out == "123"


# if the page_title length == 30, the app title should be included
def test_page_title_less_than_30_chars_includes_app_title():
    page_title = "X" * 24
    tpl = "{{ page_title | prepare_page_title }}"
    ctx = {
        "page_title": page_title,
        "content": {"app": {"title": "Request a military service record"}},
    }
    out = render_with_filter(tpl, ctx)
    assert out == page_title + " - " + ctx["content"]["app"]["title"]


# if page_title length >= 25
def test_page_title_25_chars_excludes_app_title():
    page_title = "Y" * 25
    tpl = "{{ page_title | prepare_page_title }}"
    ctx = {
        "page_title": page_title,
        "content": {"app": {"title": "Request a military service record"}},
    }
    out = render_with_filter(tpl, ctx)
    assert out == page_title
