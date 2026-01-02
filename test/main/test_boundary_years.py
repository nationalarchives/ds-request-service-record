from datetime import datetime
from unittest.mock import patch
from app.lib.boundary_years import BoundaryYears


class TestBoundaryYears:
    def test_earliest_birth_year_constant(self):
        assert BoundaryYears.EARLIEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE == 1800

    def test_latest_birth_year_constant(self):
        assert BoundaryYears.LATEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE == 1939

    def test_years_a_record_remains_closed_constant(self):
        assert BoundaryYears.YEARS_A_RECORD_REMAINS_CLOSED == 115

    def test_year_from_which_proof_of_death_is_required_with_current_year(self):
        result = BoundaryYears.last_birth_year_for_record_to_be_open(2024)
        assert result == 1908

    def test_year_from_which_proof_of_death_is_required_with_different_year(self):
        result = BoundaryYears.last_birth_year_for_record_to_be_open(2030)
        assert result == 1914

    def test_year_from_which_proof_of_death_is_required_without_current_year(self):
        with patch("app.lib.boundary_years.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 6, 15)
            result = BoundaryYears.last_birth_year_for_record_to_be_open()
            assert result == 1909

    def test_year_from_which_proof_of_death_is_required_uses_correct_calculation(self):
        # Test that the calculation is: current_year - (YEARS_A_RECORD_REMAINS_CLOSED + 1)
        test_year = 2023
        expected = test_year - (BoundaryYears.YEARS_A_RECORD_REMAINS_CLOSED + 1)
        result = BoundaryYears.last_birth_year_for_record_to_be_open(test_year)
        assert result == expected
