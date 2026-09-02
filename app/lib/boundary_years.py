from datetime import datetime, timezone


class BoundaryYears:
    EARLIEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE = 1800
    LATEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE = 1939
    YEARS_A_RECORD_REMAINS_CLOSED = 115

    @classmethod
    def first_birth_year_for_closed_records(
        cls, current_year: int | None = None
    ) -> int:
        if current_year is None:
            current_year = datetime.now(timezone.utc).year
        return current_year - cls.YEARS_A_RECORD_REMAINS_CLOSED
