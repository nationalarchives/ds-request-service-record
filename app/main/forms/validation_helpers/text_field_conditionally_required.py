from wtforms.validators import ValidationError


def text_field_required_unless_radio_has_specific_selection(
    radio_field_name, permissible_selection, message=None
):
    def _validator(form, field):
        radio = getattr(form, radio_field_name, None)

        if radio and radio.data:
            # If radio selection is NOT the permissible value
            if radio.data != permissible_selection:
                # Check if the text field is empty
                if not field.data or not str(field.data).strip():
                    raise ValidationError(message or "This field is required.")

    return _validator
