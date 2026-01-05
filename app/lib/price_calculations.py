import requests
from app.constants import OrderFeesPence
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

    response = requests.post(
        current_app.config["DELIVERY_FEE_API_URL"],
        json=payload,
        headers={"Content-Type": "application/json"},
    )

    if response.status_code != 200:
        current_app.logger.error(
            f"Failed to get delivery fee: {response.status_code} - {response.text}"
        )
        raise ValueError("Could not retrieve delivery fee")

    response_data = response.json()
    return round(float(response_data) * 100)  # Convert pounds to pence


def calculate_amount_based_on_form_data(form_data: dict) -> int:
    delivery_type = get_delivery_type(form_data)
    processing_option = form_data.get("processing_option", "standard")
    amount = 0

    if processing_option not in OPTION_MAP:
        raise ValueError("Invalid processing option")

    amount = OPTION_MAP[processing_option].get(delivery_type)

    if processing_option == "standard" and delivery_type == "PrintedTracked":
        if country := form_data.get("requester_country"):
            amount += calculate_delivery_fee(country)
        else:
            raise ValueError("Country is required for printed delivery")

    if amount is None:
        raise ValueError("Invalid processing option")

    return amount


def prepare_order_summary_data(form_data: dict) -> dict:
    processing_option = form_data.get("processing_option", "standard")
    delivery_type = get_delivery_type(form_data)

    order_summary_data = {
        "processing_option": processing_option,
        "delivery_type": delivery_type,
        "amount_pence": calculate_amount_based_on_form_data(form_data),
    }

    return order_summary_data


def get_delivery_type(form_data: dict) -> str:
    delivery_type = form_data.get("delivery_type")
    if not delivery_type:
        delivery_type = (
            "PrintedTracked" if form_data.get("does_not_have_email") else "Digital"
        )

    return delivery_type
