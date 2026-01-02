from datetime import datetime


class BoundaryYears:
    EARLIEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE = 1800
    LATEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE = 1939
    YEARS_A_RECORD_REMAINS_CLOSED = 115

    @classmethod
    def last_birth_year_for_record_to_be_open(cls, current_year: int = None) -> int:
        if current_year is None:
            current_year = datetime.now().year
        # We add 1 because the calculation is for the year after which records are closed
        return current_year - (cls.YEARS_A_RECORD_REMAINS_CLOSED + 1)
