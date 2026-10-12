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
    s = "[Take survey](external:Survey)"
    expected = '<a href="https://example.com/survey" target="_blank" rel="noreferrer noopener">Take survey</a>'
    assert inject_unique_survey_link(s) == expected


@pytest.mark.parametrize(
    "s,error_message",
    [
        (
            "[Go](https://site.example/path)",
            "external:EXTERNAL_LINK_NAME or route:ROUTE_NAME",
        ),
        (
            "[Go](external:NotDefined)",
            "ExternalLinks constant after 'external:'",
        ),
        (
            "[Go](route:PROVIDE_A_PROOF_OF_DEATH)",
            "Survey markdown links must use external:EXTERNAL_LINK_NAME targets",
        ),
    ],
)
def test_rejects_invalid_survey_link_targets(s, error_message):
    with pytest.raises(ValueError, match=error_message):
        inject_unique_survey_link(s)


def test_appends_current_page_query_param_when_path_provided_simple():
    s = "[Survey](external:Survey)"
    path = "main.before_you_start"
    expected = '<a href="https://example.com/survey?current_page=before_you_start" target="_blank" rel="noreferrer noopener">Survey</a>'
    assert inject_unique_survey_link(s, current_endpoint=path) == expected


def test_does_not_append_query_when_path_becomes_empty_after_strip():
    s = "[Survey](external:Survey)"
    path = "main."
    expected = '<a href="https://example.com/survey" target="_blank" rel="noreferrer noopener">Survey</a>'
    assert inject_unique_survey_link(s, current_endpoint=path) == expected
