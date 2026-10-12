from datetime import UTC, datetime
from unittest.mock import patch

from app.lib.boundary_years import BoundaryYears


class TestBoundaryYears:
    def test_earliest_birth_year_constant(self):
        assert BoundaryYears.EARLIEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE == 1800

    def test_latest_birth_year_constant(self):
        assert BoundaryYears.LATEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE == 1939

    def test_years_a_record_remains_closed_constant(self):
        assert BoundaryYears.YEARS_AFTER_BIRTH_RECORD_REMAINS_CLOSED == 115

    def test_years_after_birth_proof_of_death_required_for_standard_order_constant(
        self,
    ):
        assert (
            BoundaryYears.YEARS_AFTER_BIRTH_PROOF_OF_DEATH_REQUIRED_FOR_STANDARD_ORDER
            == 100
        )

    def test_first_birth_year_for_closed_records_with_supplied_year(self):
        result = BoundaryYears.first_birth_year_for_closed_records(2030)
        assert result == 1915

    def test_first_birth_year_for_closed_records_without_supplied_year(self):
        with patch("app.lib.boundary_years.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 1, 23, tzinfo=UTC)
            result = BoundaryYears.first_birth_year_for_closed_records()
            assert result == 1911

    def test_first_birth_year_for_closed_records_uses_correct_calculation(self):
        test_year = 2023
        expected = test_year - BoundaryYears.YEARS_AFTER_BIRTH_RECORD_REMAINS_CLOSED
        result = BoundaryYears.first_birth_year_for_closed_records(test_year)
        assert result == expected

    def test_first_birth_year_standard_orders_require_proof_of_death_with_supplied_year(
        self,
    ):
        result = BoundaryYears.first_birth_year_standard_orders_require_proof_of_death(
            2030
        )
        assert result == 1930

    def test_first_birth_year_standard_orders_require_proof_of_death_without_supplied_year(
        self,
    ):
        with patch("app.lib.boundary_years.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 1, 23, tzinfo=UTC)
            result = (
                BoundaryYears.first_birth_year_standard_orders_require_proof_of_death()
            )
            assert result == 1926

    def test_first_birth_year_standard_orders_require_proof_of_death_uses_correct_calculation(
        self,
    ):
        test_year = 2023
        expected = (
            test_year
            - BoundaryYears.YEARS_AFTER_BIRTH_PROOF_OF_DEATH_REQUIRED_FOR_STANDARD_ORDER
        )
        result = BoundaryYears.first_birth_year_standard_orders_require_proof_of_death(
            test_year
        )
        assert result == expected
