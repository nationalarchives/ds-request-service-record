from app.constants import ORDER_TYPES


def get_order_summary_template_variant(order_summary_data):
    """
    Determines which order summary template variant to render based on
    processing option and delivery type.

    Args:
        order_summary_data: Dictionary containing order summary information
                           with keys 'processing_option', 'delivery_type', 'service_branch', and 'were_they_a_commissioned_officer'.

    Returns:
        str: Template variant name (one of:
            your-order-summary-standard-printed,
            your-order-summary-standard-digital,
            your-order-summary-full-record-check-printed,
            your-order-summary-full-record-check-digital,
            your-order-summary-full-record-check-british-army-officer-digital,
            your-order-summary-full-record-check-british-army-officer-printed)

    Raises:
        ValueError: If processing_option or delivery_type are invalid
    """
    processing_option = order_summary_data.get("processing_option")
    delivery_type = order_summary_data.get("delivery_type")
    service_branch = order_summary_data.get("service_branch")
    were_they_a_commissioned_officer = order_summary_data.get(
        "were_they_a_commissioned_officer"
    )

    if (
        processing_option == "full"
        and delivery_type == "Digital"
        and service_branch == "BRITISH_ARMY"
        and were_they_a_commissioned_officer == "yes"
    ):
        return "your-order-summary-full-record-check-british-army-officer-digital"

    if (
        processing_option == "full"
        and delivery_type == "PrintedTracked"
        and service_branch == "BRITISH_ARMY"
        and were_they_a_commissioned_officer == "yes"
    ):
        return "your-order-summary-full-record-check-british-army-officer-printed"

    # Validate that the combination exists in ORDER_TYPES
    key = (processing_option, delivery_type)
    if key not in ORDER_TYPES:
        valid_combinations = list(ORDER_TYPES.keys())
        raise ValueError(
            f"Invalid combination: processing_option='{processing_option}', "
            f"delivery_type='{delivery_type}'. "
            f"Must be one of {valid_combinations}"
        )

    # Map combinations to template variants
    template_mapping = {
        ("standard", "PrintedTracked"): "your-order-summary-standard-printed",
        ("standard", "Digital"): "your-order-summary-standard-digital",
        ("full", "PrintedTracked"): "your-order-summary-full-record-check-printed",
        ("full", "Digital"): "your-order-summary-full-record-check-digital",
    }

    return template_mapping[key]
