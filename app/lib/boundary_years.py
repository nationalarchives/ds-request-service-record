from datetime import UTC, datetime


class BoundaryYears:
    EARLIEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE = 1800
    LATEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE = 1939
    # The number of years after a service person's birth that
    # their military service record remains closed to the public.
    YEARS_AFTER_BIRTH_RECORD_REMAINS_CLOSED = 115
    # The number of years after a service person's birth that
    # proof of death is required for a standard order
    YEARS_AFTER_BIRTH_PROOF_OF_DEATH_REQUIRED_FOR_STANDARD_ORDER = 100

    @classmethod
    def first_birth_year_for_closed_records(
        cls, current_year: int | None = None
    ) -> int:
        if current_year is None:
            current_year = datetime.now(UTC).year
        return current_year - cls.YEARS_AFTER_BIRTH_RECORD_REMAINS_CLOSED

    @classmethod
    def first_birth_year_standard_orders_require_proof_of_death(
        cls, current_year: int | None = None
    ) -> int:
        if current_year is None:
            current_year = datetime.now(UTC).year
        return (
            current_year
            - cls.YEARS_AFTER_BIRTH_PROOF_OF_DEATH_REQUIRED_FOR_STANDARD_ORDER
        )
