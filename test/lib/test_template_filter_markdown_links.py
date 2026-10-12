import pytest

from app.constants import ExternalLinks
from app.lib.template_filters import parse_markdown_links


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            "Try [Ancestry](ANCESTRY_SEARCH) before continuing",
            f'Try <a href="{ExternalLinks.ANCESTRY_SEARCH}" target="_blank" rel="noreferrer noopener">Ancestry</a> before continuing',
        ),
        (
            "Mix: [FOI](FOI_REQUEST_GUIDANCE) and [Contact us](CONTACT_US)",
            f'Mix: <a href="{ExternalLinks.FOI_REQUEST_GUIDANCE}" target="_blank" rel="noreferrer noopener">FOI</a> and <a href="{ExternalLinks.CONTACT_US}" target="_blank" rel="noreferrer noopener">Contact us</a>',
        ),
        ("No links here!", "No links here!"),
    ],
)
def test_parse_markdown_links_default_new_tab(input_str, expected):
    assert parse_markdown_links(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            "Try [Ancestry](ANCESTRY_SEARCH) before continuing",
            f'Try <a href="{ExternalLinks.ANCESTRY_SEARCH}">Ancestry</a> before continuing',
        ),
        (
            "Mix: [FOI](FOI_REQUEST_GUIDANCE) and [Contact us](CONTACT_US)",
            f'Mix: <a href="{ExternalLinks.FOI_REQUEST_GUIDANCE}">FOI</a> and <a href="{ExternalLinks.CONTACT_US}">Contact us</a>',
        ),
        ("No links here!", "No links here!"),
    ],
)
def test_parse_markdown_links_no_new_tab(input_str, expected):
    assert parse_markdown_links(input_str, new_tab=False) == expected


@pytest.mark.parametrize(
    "input_str",
    [
        "Raw URL [Example](https://example.com)",
        "Unknown constant [Example](NOT_A_REAL_LINK)",
    ],
)
def test_parse_markdown_links_rejects_non_external_links(input_str):
    with pytest.raises(ValueError, match="ExternalLinks constant"):
        parse_markdown_links(input_str)
