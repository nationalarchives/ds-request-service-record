import requests
from flask import current_app

from app.constants import ORDER_TYPES
from app.lib.price_calculations import (
    calculate_base_fee,
    calculate_delivery_fee,
    get_delivery_type,
)


def prepare_order_summary_data(form_data: dict) -> dict:
    if not form_data:
        current_app.logger.error("prepare_order_summary_data called with no form data")
        return None

    processing_option = form_data.get("processing_option", "standard")
    delivery_type = get_delivery_type(form_data)

    try:
        base_fee = calculate_base_fee(processing_option, delivery_type)
    except ValueError as e:
        current_app.logger.error(f"Error in base fee calculation: {e}")
        return None

    try:
        delivery_fee_pence = (
            calculate_delivery_fee(form_data.get("requester_country"))
            if processing_option == "standard" and delivery_type == "PrintedTracked"
            else 0
        )
    except (requests.RequestException, KeyError, ValueError) as e:
        current_app.logger.error(f"Error in delivery fee calculation: {e}")
        return None

    order_type = ORDER_TYPES.get((processing_option, delivery_type))

    order_summary_data = {
        "processing_option": processing_option,
        "delivery_type": delivery_type,
        "amount_pence": base_fee,
        "delivery_fee_pence": delivery_fee_pence,
        "order_type": order_type,
    }

    return order_summary_data
