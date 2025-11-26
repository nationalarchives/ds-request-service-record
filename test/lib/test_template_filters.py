import pytest
from app.lib.template_filters import parse_markdown_links


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            "My favorite organisation is [The National Archives](https://www.nationalarchives.gov.uk) in Kew",
            'My favorite organisation is <a href="https://www.nationalarchives.gov.uk" target="_blank" rel="noreferrer noopener">The National Archives</a> in Kew',
        ),
        ("No links here!", "No links here!"),
        (
            "Multiple: [GOV.UK](https://www.gov.uk) and [Example](https://example.com)",
            'Multiple: <a href="https://www.gov.uk" target="_blank" rel="noreferrer noopener">GOV.UK</a> and <a href="https://example.com" target="_blank" rel="noreferrer noopener">Example</a>',
        ),
        (
            "Edge [case](http://example.com) with [brackets] inside [text](http://test.com)",
            'Edge <a href="http://example.com" target="_blank" rel="noreferrer noopener">case</a> with [brackets] inside <a href="http://test.com" target="_blank" rel="noreferrer noopener">text</a>',
        ),
        (
            "[Just a link](http://example.com)",
            '<a href="http://example.com" target="_blank" rel="noreferrer noopener">Just a link</a>',
        ),
        ("Empty []() should not break", "Empty []() should not break"),
        (
            "Try [Ancestry](ANCESTRY_SEARCH)",
            'Try <a href="https://www.ancestry.co.uk/search/" target="_blank" rel="noreferrer noopener">Ancestry</a>',
        ),
        # Mixed external key and plain URL
        (
            "Mix: [FOI](FOI_REQUEST_GUIDANCE) and [The National Archives](https://www.nationalarchives.gov.uk)",
            'Mix: <a href="https://www.gov.uk/make-a-freedom-of-information-request" target="_blank" rel="noreferrer noopener">FOI</a> and <a href="https://www.nationalarchives.gov.uk" target="_blank" rel="noreferrer noopener">The National Archives</a>',
        ),
    ],
)
def test_parse_markdown_links(input_str, expected):
    assert parse_markdown_links(input_str) == expected
