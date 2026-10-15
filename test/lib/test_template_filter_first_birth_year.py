from datetime import datetime, timezone
from unittest.mock import patch

from app.lib.template_filters import (
    parse_first_birth_year_for_closed_records,
    parse_first_birth_year_standard_orders_require_proof_of_death,
)


def test_returns_none_when_input_is_none():
    assert parse_first_birth_year_for_closed_records(None) is None


def test_returns_empty_string_when_input_is_empty():
    assert parse_first_birth_year_for_closed_records("") == ""


def test_replaces_first_birth_year_placeholder_with_span():
    with patch("app.lib.template_filters.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 1, 23, tzinfo=timezone.utc)

        result = parse_first_birth_year_for_closed_records(
            "Born after [FIRST_BIRTH_YEAR_FOR_CLOSED_RECORDS]"
        )

    assert (
        result
        == "Born after <span data-first-birth-year-for-closed-records='1911'>1911</span>"
    )


def test_leaves_string_unchanged_when_placeholder_not_present():
    with patch("app.lib.template_filters.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 1, 23, tzinfo=timezone.utc)

        result = parse_first_birth_year_for_closed_records("No placeholder here")

    assert result == "No placeholder here"


def test_replaces_standard_orders_proof_of_death_placeholder_with_span():
    with patch("app.lib.template_filters.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 1, 23, tzinfo=timezone.utc)

        result = parse_first_birth_year_standard_orders_require_proof_of_death(
            "Born after [FIRST_BIRTH_YEAR_STANDARD_ORDERS_REQUIRE_PROOF_OF_DEATH]"
        )

    assert (
        result
        == "Born after <span data-first-birth-year-standard-orders-require-proof-of-death='1926'>1926</span>"
    )
