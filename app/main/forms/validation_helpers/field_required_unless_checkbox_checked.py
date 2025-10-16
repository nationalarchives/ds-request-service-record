from wtforms.validators import StopValidation, ValidationError


def field_required_unless_checkbox_checked(checkbox_field_name, message=None):
    def _validator(form, field):
        checkbox = getattr(form, checkbox_field_name, None)
        if checkbox and checkbox.data:
            if not field.data:
                raise StopValidation()
        else:
            if not field.data or not str(field.data).strip():
                raise ValidationError(message or "This field is required.")

    return _validator
