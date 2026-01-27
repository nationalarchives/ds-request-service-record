import requests
from app.constants import ORDER_TYPES, OrderFeesPence
from flask import current_app

OPTION_MAP = {
    "standard": {
        "Digital": OrderFeesPence.STANDARD_DIGITAL.value,
        "PrintedTracked": OrderFeesPence.STANDARD_PRINTED.value,
    },
    "full": {
        "Digital": OrderFeesPence.FULL_DIGITAL.value,
        "PrintedTracked": OrderFeesPence.FULL_PRINTED.value,
    },
}


def calculate_delivery_fee(country: str) -> int:
    payload = {"A3Colour": 10, "Country": country, "IsTracking": True}

    try:
        response = requests.post(
            current_app.config["DELIVERY_FEE_API_URL"],
            json=payload,
            headers={"Content-Type": "application/json"},
        )

        response.raise_for_status()
        response_data = response.json()

        # Convert pounds to pence
        return round(float(response_data) * 100)
    except requests.RequestException as e:
        current_app.logger.error(f"Error while getting delivery fee: {e}")
        raise e
    except (ValueError, KeyError) as e:
        current_app.logger.error(f"Error calculating delivery fee response: {e}")
        raise e


def calculate_base_fee(processing_option: str, delivery_type: str) -> int:
    if processing_option not in OPTION_MAP:
        current_app.logger.error(f"Invalid processing option: {processing_option}")
        raise ValueError("Invalid processing option")

    amount = OPTION_MAP[processing_option].get(delivery_type)

    if amount is None:
        current_app.logger.error(f"Invalid delivery type: {delivery_type}")
        raise ValueError("Invalid delivery type")

    return amount


def calculate_amount_based_on_form_data(form_data: dict) -> int:
    delivery_type = get_delivery_type(form_data)
    processing_option = form_data.get("processing_option", "standard")

    try:
        amount = calculate_base_fee(processing_option, delivery_type)
    except ValueError as e:
        raise e

    if processing_option == "standard" and delivery_type == "PrintedTracked":
        if country := form_data.get("requester_country"):
            try:
                delivery_fee = calculate_delivery_fee(country)
            except Exception as e:
                raise e
            amount += delivery_fee
        else:
            raise ValueError("Country is required for printed delivery")

    if amount is None:
        raise ValueError("Could not calculate amount")

    return amount


def prepare_order_summary_data(form_data: dict) -> dict:
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
    except Exception as e:
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


def get_delivery_type(form_data: dict) -> str:
    delivery_type = form_data.get("delivery_type")
    if not delivery_type:
        delivery_type = (
            "PrintedTracked" if form_data.get("does_not_have_email") else "Digital"
        )

    return delivery_type
