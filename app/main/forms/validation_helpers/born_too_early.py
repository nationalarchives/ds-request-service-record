import datetime

from wtforms.validators import ValidationError
from app.lib.boundary_years import BoundaryYears


class BornTooEarly:
    """
    Validates a date is in not before a given year.

    :param message:
        Error message to raise in case of a validation error.
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext(
                f"Year of birth must be {BoundaryYears.EARLIEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE} or later."
            )
        try:
            if not field.data:
                raise ValidationError(message)
            try:
                field_date = field.data.date()
            except AttributeError:
                field_date = field.data
            if type(field_date) is not datetime.date:
                try:
                    field_date = datetime.date.fromisoformat(field.data)
                except Exception:
                    raise ValueError()
            if field_date < datetime.date(
                    BoundaryYears.EARLIEST_SERVICE_PERSON_BIRTH_YEAR_FOR_THIS_SERVICE,
                    1,
                    1,
            ):
                raise ValueError(message)
        except ValueError as exc:
            raise ValidationError(message) from exc
