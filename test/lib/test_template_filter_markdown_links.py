import pytest
from app.lib.template_filters import parse_markdown_links


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            "My favorite organisation is [The National Archive](https://www.nationalarchives.gov.uk)",
            'My favorite organisation is <a href="https://www.nationalarchives.gov.uk" target="_blank" rel="noreferrer noopener">The National Archive</a>',
        ),
        ("No links here!", "No links here!"),
        (
            "Multiple: [GOV.UK](https://www.gov.uk) and [The National Archives](https://www.nationalarchives.gov.uk)",
            'Multiple: <a href="https://www.gov.uk" target="_blank" rel="noreferrer noopener">GOV.UK</a> and <a href="https://www.nationalarchives.gov.uk" target="_blank" rel="noreferrer noopener">The National Archives</a>',
        ),
        (
            "Edge [case](http://example.com) with [brackets] inside [text](http://test.com)",
            'Edge <a href="http://example.com" target="_blank" rel="noreferrer noopener">case</a> with [brackets] inside <a href="http://test.com" target="_blank" rel="noreferrer noopener">text</a>',
        ),
        (
            "[Just a link](http://only.com)",
            '<a href="http://only.com" target="_blank" rel="noreferrer noopener">Just a link</a>',
        ),
        ("Empty []() should not break", "Empty []() should not break"),
        (
            "Try [Ancestry](ANCESTRY_SEARCH) before continuing",
            'Try <a href="https://www.ancestry.co.uk/search/categories/mil_draft/" target="_blank" rel="noreferrer noopener">Ancestry</a> before continuing',
        ),
        (
            "Mix: [FOI](FOI_REQUEST_GUIDANCE) and [DDG](https://www.nationalarchives.gov.uk)",
            'Mix: <a href="https://www.gov.uk/make-a-freedom-of-information-request" target="_blank" rel="noreferrer noopener">FOI</a> and <a href="https://www.nationalarchives.gov.uk" target="_blank" rel="noreferrer noopener">DDG</a>',
        ),
    ],
)
def test_parse_markdown_links_default_new_tab(input_str, expected):
    assert parse_markdown_links(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            "My favorite organisation is [The National Archive](https://www.nationalarchives.gov.uk)",
            'My favorite organisation is <a href="https://www.nationalarchives.gov.uk">The National Archive</a>',
        ),
        ("No links here!", "No links here!"),
        (
            "Multiple: [GOV.UK](https://www.gov.uk) and [The National Archives](https://www.nationalarchives.gov.uk)",
            'Multiple: <a href="https://www.gov.uk">GOV.UK</a> and <a href="https://www.nationalarchives.gov.uk">The National Archives</a>',
        ),
        (
            "Edge [case](http://example.com) with [brackets] inside [text](http://test.com)",
            'Edge <a href="http://example.com">case</a> with [brackets] inside <a href="http://test.com">text</a>',
        ),
        (
            "[Just a link](http://only.com)",
            '<a href="http://only.com">Just a link</a>',
        ),
        ("Empty []() should not break", "Empty []() should not break"),
        (
            "Try [Ancestry](ANCESTRY_SEARCH) before continuing",
            'Try <a href="https://www.ancestry.co.uk/search/categories/mil_draft/">Ancestry</a> before continuing',
        ),
        (
            "Mix: [FOI](FOI_REQUEST_GUIDANCE) and [DDG](https://www.nationalarchives.gov.uk)",
            'Mix: <a href="https://www.gov.uk/make-a-freedom-of-information-request">FOI</a> and <a href="https://www.nationalarchives.gov.uk">DDG</a>',
        ),
    ],
)
def test_parse_markdown_links_no_new_tab(input_str, expected):
    assert parse_markdown_links(input_str, new_tab=False) == expected
