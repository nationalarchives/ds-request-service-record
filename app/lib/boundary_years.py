from datetime import datetime


class BoundaryYears:
    """Define year boundaries for service record availability and record closure.

    Service records are only available for people born between specific years,
    and records remain closed for 115 years after the person's birth.
    """

    EARLIEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE = 1800
    LATEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE = 1939
    YEARS_A_RECORD_REMAINS_CLOSED = 115

    @classmethod
    def last_birth_year_for_record_to_be_open(cls, current_year: int = None) -> int:
        """Calculate the last birth year for which records are now open to the public.

        Records remain closed for 115 years after birth, so this calculates
        which birth year records became open most recently.

        Args:
            current_year (int): Year to calculate from; defaults to current year

        Returns:
            int: The last birth year for which records are open
        """
        if current_year is None:
            current_year = datetime.now().year
        # Add 1 because the calculation is for the year after which records are closed
        return current_year - (cls.YEARS_A_RECORD_REMAINS_CLOSED + 1)
