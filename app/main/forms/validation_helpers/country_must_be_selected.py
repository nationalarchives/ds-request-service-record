from wtforms.validators import ValidationError
from app.lib.content import load_content, get_field_content


def country_must_be_selected(message=None):

    content = load_content()

    def _validator(form, field):
        if field.data == get_field_content(
            content, "requester_country", "prompt_to_select"
        ):
            raise ValidationError(message or "Please select a country")

    return _validator
