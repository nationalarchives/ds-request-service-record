import pytest
from app.lib.template_filters import parse_markdown_links


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            "My favorite search engine is [Duck Duck Go](https://duckduckgo.com)",
            'My favorite search engine is <a href="https://duckduckgo.com">Duck Duck Go</a>',
        ),
        ("No links here!", "No links here!"),
        (
            "Multiple: [Google](https://google.com) and [Bing](https://bing.com)",
            'Multiple: <a href="https://google.com">Google</a> and <a href="https://bing.com">Bing</a>',
        ),
        (
            "Edge [case](http://example.com) with [brackets] inside [text](http://test.com)",
            'Edge <a href="http://example.com">case</a> with [brackets] inside <a href="http://test.com">text</a>',
        ),
        ("[Just a link](http://only.com)", '<a href="http://only.com">Just a link</a>'),
        ("Empty []() should not break", "Empty []() should not break"),
    ],
)
def test_parse_markdown_links(input_str, expected):
    assert parse_markdown_links(input_str) == expected
