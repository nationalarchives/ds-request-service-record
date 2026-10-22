"""
Business rules relating to service person date of birth.

`BoundaryYears` provides the raw threshold values. `DateOfBirthRules` turns
those thresholds into domain decisions like "is the supplied date of birth too late
for this service?" or "should we show a warning before a user selects Full record check?".
"""

from datetime import date, datetime, timezone

from app.lib.boundary_years import BoundaryYears


class DateOfBirthRules:
    """Pure rule functions for DOB-driven decisions.

    These methods are intentionally free of route or form state. They answer a
    single business question based on a DOB and the current year, making them easy
    to test and safe to call from route handlers and the state machine.
    """

    @staticmethod
    def is_born_too_late(
        date_of_birth: date | None, current_year: int | None = None
    ) -> bool:
        """Return True when a person was born after the latest birth year."""
        date_of_birth, current_year = DateOfBirthRules._normalise_dob_and_year(
            date_of_birth, current_year
        )
        if date_of_birth is None:
            return False

        return (
            date_of_birth.year
            > BoundaryYears.LATEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE
        )

    @staticmethod
    def requires_proof_of_death_for_standard_order(
        date_of_birth: date | None, current_year: int | None = None
    ) -> bool:
        """Return True when Standard requests will require a proof of death."""
        date_of_birth, current_year = DateOfBirthRules._normalise_dob_and_year(
            date_of_birth, current_year
        )
        if date_of_birth is None:
            return False

        return (
            date_of_birth.year
            >= BoundaryYears.first_birth_year_standard_orders_require_proof_of_death(
                current_year
            )
        )

    @staticmethod
    def requires_proof_of_death_for_full_record_check(
        date_of_birth: date | None, current_year: int | None = None
    ) -> bool:
        """Return True when a Full record check will require proof of death."""
        date_of_birth, current_year = DateOfBirthRules._normalise_dob_and_year(
            date_of_birth, current_year
        )
        if date_of_birth is None:
            return False

        return date_of_birth.year >= BoundaryYears.first_birth_year_for_closed_records(
            current_year
        )

    @staticmethod
    def show_proof_of_death_warning(
        date_of_birth: date | None, current_year: int | None = None
    ) -> bool:
        """Return True when DOB falls in the warning window.

        The warning window covers the period after records become closed to the
        public but before standard orders require a proof of death. It is used to
        alert the user before they continue with a Full record check.
        """
        date_of_birth, current_year = DateOfBirthRules._normalise_dob_and_year(
            date_of_birth, current_year
        )
        if date_of_birth is None:
            return False

        first_birth_year_for_closed_records = (
            BoundaryYears.first_birth_year_for_closed_records(current_year)
        )
        first_birth_year_for_standard_order_proof = (
            BoundaryYears.first_birth_year_standard_orders_require_proof_of_death(
                current_year
            )
        )

        return (
            first_birth_year_for_closed_records
            < date_of_birth.year
            < first_birth_year_for_standard_order_proof
        )

    @staticmethod
    def _normalise_dob_and_year(
        date_of_birth: date | None, current_year: int | None = None
    ) -> tuple[date | None, int | None]:
        """Return a valid DOB and the current year, normalising missing values."""
        if not date_of_birth:
            return None, None

        if current_year is None:
            current_year = datetime.now(timezone.utc).year

        return date_of_birth, current_year
