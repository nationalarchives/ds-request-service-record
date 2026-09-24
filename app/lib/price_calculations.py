import requests
from flask import current_app

from app.constants import OrderFeesPence

OPTION_MAP = {
    "standard": {
        "Digital": OrderFeesPence.STANDARD_DIGITAL,
        "PrintedTracked": OrderFeesPence.STANDARD_PRINTED,
    },
    "full": {
        "Digital": OrderFeesPence.FULL_DIGITAL,
        "PrintedTracked": OrderFeesPence.FULL_PRINTED,
    },
}


def calculate_delivery_fee(country: str) -> int:
    payload = {"A3Colour": 10, "Country": country, "IsTracking": True}

    response = requests.post(
        current_app.config["DELIVERY_FEE_API_URL"],
        json=payload,
        headers={"Content-Type": "application/json"},
    )

    response.raise_for_status()
    response_data = response.json()

    # Convert pounds to pence
    return round(float(response_data) * 100)


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

    amount = calculate_base_fee(processing_option, delivery_type)

    if processing_option == "standard" and delivery_type == "PrintedTracked":
        if country := form_data.get("requester_country"):
            delivery_fee = calculate_delivery_fee(country)
            amount += delivery_fee
        else:
            raise ValueError("Country is required for printed delivery")

    if amount is None:
        raise ValueError("Could not calculate amount")

    return amount


def get_delivery_type(form_data: dict) -> str:
    delivery_type = form_data.get("delivery_type")
    if not delivery_type:
        delivery_type = (
            "PrintedTracked" if form_data.get("does_not_have_email") else "Digital"
        )

    return delivery_type
