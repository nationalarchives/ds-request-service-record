from wtforms.validators import ValidationError


def radio_conditionally_required(
    other_field_name=None, other_field_value=None, message=None
):
    """
    Returns a WTForms validator that makes the current field required only if another
    field (identified by `other_field_name`) has a specific value (`other_field_value`).

    Parameters:
        other_field_name (str): Name of the sibling field whose value we inspect.
        other_field_value (Any): Value that triggers the requirement.
        message (str): Error message raised if requirement is not met.

    Behavior:
        - If the other field does not exist on the form, validator silently does nothing.
        - If the other field's value equals `other_field_value` AND current field is empty,
          a ValidationError is raised.
        - Otherwise, validation passes.
    """
    if message is None:
        message = "This field is required."

    def _validator(form, field):
        # Attempt to get the other_field from the form
        other_field = getattr(form, other_field_name, None)
        # Fail silently if other_field does not exist
        if other_field is None:
            return
        # The key logic:
        # if other_field has the specified value and current field is empty,
        # raise a ValidationError
        if other_field.data == other_field_value and not field.data:
            raise ValidationError(message)

    return _validator
