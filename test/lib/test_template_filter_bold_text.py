import pytest
from app.lib.template_filters import parse_bold_text


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("This is **bold** text.", "This is <strong>bold</strong> text."),
        ("No bold here.", "No bold here."),
        (
            "**Bold at start** of sentence.",
            "<strong>Bold at start</strong> of sentence.",
        ),
        ("End of sentence **bold**.", "End of sentence <strong>bold</strong>."),
        (
            "Multiple **bold** words **here**.",
            "Multiple <strong>bold</strong> words <strong>here</strong>.",
        ),
        (
            "Nested **bold with **asterisks** inside**.",
            "Nested <strong>bold with </strong>asterisks<strong> inside</strong>.",
        ),
        ("Edge case with no closing **bold.", "Edge case with no closing **bold."),
        ("Empty **** should not break.", "Empty **** should not break."),
    ],
)
def test_parse_bold_text(input_str, expected):
    assert parse_bold_text(input_str) == expected
