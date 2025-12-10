from wtforms.validators import ValidationError


def field_must_be_empty_if_checkbox_checked(checkbox_field_name, message=None):
    def _validator(form, field):
        checkbox = getattr(form, checkbox_field_name, None)
        if checkbox and checkbox.data:
            if field.data and str(field.data).strip():
                raise ValidationError(
                    message or "This field must be empty when the checkbox is checked."
                )

    return _validator
