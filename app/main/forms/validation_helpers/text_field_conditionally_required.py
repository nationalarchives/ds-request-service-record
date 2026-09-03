from wtforms.validators import ValidationError


def text_field_required_unless_radio_has_specific_selection(
    radio_field_name, permissible_selection, message=None
):
    def _validator(form, field):
        radio = getattr(form, radio_field_name, None)

        # Validate when a non-permissible radio option is selected and text is empty.
        if (
            radio
            and radio.data
            and radio.data != permissible_selection
            and (not field.data or not str(field.data).strip())
        ):
            raise ValidationError(message or "This field is required.")

    return _validator
