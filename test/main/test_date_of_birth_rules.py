from datetime import date

from app.lib.date_of_birth_rules import DateOfBirthRules


class TestDateOfBirthRules:
    def test_date_of_birth_rules_requires_proof_of_death_for_standard_order(self):
        assert (
            DateOfBirthRules.requires_proof_of_death_for_standard_order(
                date(1926, 1, 1), current_year=2026
            )
            is True
        )
        assert (
            DateOfBirthRules.requires_proof_of_death_for_standard_order(
                date(1925, 1, 1), current_year=2026
            )
            is False
        )

    def test_date_of_birth_rules_requires_proof_of_death_for_full_record_check(self):
        assert (
            DateOfBirthRules.requires_proof_of_death_for_full_record_check(
                date(1911, 1, 1), current_year=2026
            )
            is True
        )
        assert (
            DateOfBirthRules.requires_proof_of_death_for_full_record_check(
                date(1910, 1, 1), current_year=2026
            )
            is False
        )

    def test_date_of_birth_rules_should_show_proof_of_death_warning(self):
        assert (
            DateOfBirthRules.show_proof_of_death_warning(
                date(1912, 1, 1), current_year=2026
            )
            is True
        )
        assert (
            DateOfBirthRules.show_proof_of_death_warning(
                date(1925, 1, 1), current_year=2026
            )
            is True
        )
        assert (
            DateOfBirthRules.show_proof_of_death_warning(
                date(1926, 1, 1), current_year=2026
            )
            is False
        )
        assert (
            DateOfBirthRules.show_proof_of_death_warning(
                date(1911, 1, 1), current_year=2026
            )
            is False
        )

    def test_date_of_birth_rules_is_born_too_late(self):
        assert (
            DateOfBirthRules.is_born_too_late(date(1940, 1, 1), current_year=2026)
            is True
        )
        assert (
            DateOfBirthRules.is_born_too_late(date(1939, 1, 1), current_year=2026)
            is False
        )
