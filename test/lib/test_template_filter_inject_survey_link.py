import pytest
from app.lib.template_filters import inject_unique_survey_link

MODULE_PATH = "app.lib.template_filters"


@pytest.fixture(autouse=True)
def mock_external_links(monkeypatch):
    class MockExternalLinks:
        Survey = "https://example.com/survey"
        Feedback = "https://example.com/feedback"

    monkeypatch.setattr(f"{MODULE_PATH}.ExternalLinks", MockExternalLinks, raising=True)


def test_returns_none_when_input_none():
    assert inject_unique_survey_link(None) is None


def test_returns_empty_when_input_empty_string():
    assert inject_unique_survey_link("") == ""


def test_no_markdown_links_returns_original_string():
    s = "No links here."
    assert inject_unique_survey_link(s) == s


def test_replaces_markdown_link_with_anchor_without_path():
    s = "[Take survey](Survey)"
    expected = '<a href="https://example.com/survey" target="_blank" rel="noreferrer noopener">Take survey</a>'
    assert inject_unique_survey_link(s) == expected


def test_uses_raw_url_when_key_not_in_external_links():
    s = "[Go](https://site.example/path)"
    expected = '<a href="https://site.example/path" target="_blank" rel="noreferrer noopener">Go</a>'
    assert inject_unique_survey_link(s) == expected


def test_appends_current_page_query_param_when_path_provided_simple():
    s = "[Survey](Survey)"
    path = "main.before_you_start"
    expected = '<a href="https://example.com/survey?current_page=before_you_start" target="_blank" rel="noreferrer noopener">Survey</a>'
    assert inject_unique_survey_link(s, current_endpoint=path) == expected


def test_does_not_append_query_when_path_becomes_empty_after_strip():
    s = "[Survey](Survey)"
    path = "main."
    expected = '<a href="https://example.com/survey" target="_blank" rel="noreferrer noopener">Survey</a>'
    assert inject_unique_survey_link(s, current_endpoint=path) == expected
