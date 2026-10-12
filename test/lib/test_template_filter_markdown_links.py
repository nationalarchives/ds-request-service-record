import pytest
from flask import url_for

from app import create_app
from app.constants import ExternalLinks, MultiPageFormRoutes
from app.lib.template_filters import parse_markdown_links


@pytest.fixture
def app():
    return create_app("config.Test")


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            "Try [Ancestry](external:ANCESTRY_SEARCH) before continuing",
            f'Try <a href="{ExternalLinks.ANCESTRY_SEARCH}" target="_blank" rel="noreferrer noopener">Ancestry</a> before continuing',
        ),
        (
            "Mix: [FOI](external:FOI_REQUEST_GUIDANCE) and [Contact us](external:CONTACT_US)",
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
            "Try [Ancestry](external:ANCESTRY_SEARCH) before continuing",
            f'Try <a href="{ExternalLinks.ANCESTRY_SEARCH}">Ancestry</a> before continuing',
        ),
        (
            "Mix: [FOI](external:FOI_REQUEST_GUIDANCE) and [Contact us](external:CONTACT_US)",
            f'Mix: <a href="{ExternalLinks.FOI_REQUEST_GUIDANCE}">FOI</a> and <a href="{ExternalLinks.CONTACT_US}">Contact us</a>',
        ),
        ("No links here!", "No links here!"),
    ],
)
def test_parse_markdown_links_no_new_tab(input_str, expected):
    assert parse_markdown_links(input_str, new_tab=False) == expected


def test_parse_markdown_links_resolves_route_targets(app):
    with app.test_request_context():
        expected_url = url_for(MultiPageFormRoutes.PROVIDE_A_PROOF_OF_DEATH.value)
        parsed = parse_markdown_links(
            "Read [more about proof of death](route:PROVIDE_A_PROOF_OF_DEATH)"
        )

    assert parsed == f'Read <a href="{expected_url}">more about proof of death</a>'


def test_parse_markdown_links_can_mix_external_and_route_links(app):
    with app.test_request_context():
        route_url = url_for(MultiPageFormRoutes.PROVIDE_A_PROOF_OF_DEATH.value)
        parsed = parse_markdown_links(
            "See [proof guidance](route:PROVIDE_A_PROOF_OF_DEATH) or [contact us](external:CONTACT_US)"
        )

    assert parsed == (
        f'See <a href="{route_url}">proof guidance</a> '
        f'or <a href="{ExternalLinks.CONTACT_US}" target="_blank" rel="noreferrer noopener">contact us</a>'
    )


def test_parse_markdown_links_keeps_route_links_in_same_tab_when_new_tab_false(app):
    with app.test_request_context():
        route_url = url_for(MultiPageFormRoutes.PROVIDE_A_PROOF_OF_DEATH.value)
        parsed = parse_markdown_links(
            "See [proof guidance](route:PROVIDE_A_PROOF_OF_DEATH) or [contact us](external:CONTACT_US)",
            new_tab=False,
        )

    assert parsed == (
        f'See <a href="{route_url}">proof guidance</a> '
        f'or <a href="{ExternalLinks.CONTACT_US}">contact us</a>'
    )


@pytest.mark.parametrize(
    "input_str,error_message",
    [
        (
            "Raw URL [Example](https://example.com)",
            "external:EXTERNAL_LINK_NAME or route:ROUTE_NAME",
        ),
        (
            "Unknown constant [Example](external:NOT_A_REAL_LINK)",
            "ExternalLinks constant after 'external:'",
        ),
        (
            "Missing external constant [Example](external:   )",
            "ExternalLinks constant after 'external:'",
        ),
        (
            "Unknown route [Example](route:NOT_A_REAL_ROUTE)",
            "MultiPageFormRoutes member name after 'route:'",
        ),
        (
            "Missing route [Example](route:   )",
            "MultiPageFormRoutes member name after 'route:'",
        ),
        (
            "Unknown prefix [Example](mailto:test@example.com)",
            "external:EXTERNAL_LINK_NAME or route:ROUTE_NAME",
        ),
    ],
)
def test_parse_markdown_links_rejects_invalid_targets(app, input_str, error_message):
    with app.test_request_context(), pytest.raises(ValueError, match=error_message):
        parse_markdown_links(input_str)
