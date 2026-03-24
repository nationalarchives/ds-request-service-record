def check_for_fields_required_by_gov_uk_pay(form_data: dict, current_app) -> bool:
    """
    Validate whether `form_data` contains the minimum fields required to proceed
    to GOV.UK Pay.

    Rules:
    1. All required service person fields must be present and truthy:
       - `forenames`
       - `last_name`
       - `date_of_birth`
    2. In addition, at least one of the following must be true:
       - `requester_email` is present and truthy, or
       - all required postal fields are present and truthy:
         `requester_address1`,
         `requester_town_city`,
         `requester_postcode`,
         `requester_country`

    Args:
        form_data (dict): Submitted form values keyed by field name.
        current_app: Application object that provides `logger.warning`.

    Returns:
        bool: `True` when validation passes, otherwise `False`.

    Side Effects:
        Logs a warning when either rule is not met.
    """

    if not isinstance(form_data, dict):
        current_app.logger.warning(
            "Unable to proceed to payment because form_data is not a dict: got %s",
            type(form_data).__name__,
        )
        return False

    required_serviceperson_fields = ["forenames", "last_name", "date_of_birth"]
    required_postal_address_fields = [
        "requester_address1",
        "requester_town_city",
        "requester_postcode",
        "requester_country",
    ]

    for field in required_serviceperson_fields:
        if not form_data.get(field):
            current_app.logger.warning(
                "Unable to proceed to payment because the form_data is missing the required field: %s",
                field,
            )
            return False

    has_requester_email = bool(form_data.get("requester_email"))
    has_all_postal_fields = all(
        form_data.get(field) for field in required_postal_address_fields
    )

    if not (has_requester_email or has_all_postal_fields):
        current_app.logger.warning(
            "Unable to proceed to payment because form_data is missing requester_email or incomplete postal address fields"
        )
        return False

    return True
