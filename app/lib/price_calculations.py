from flask import current_app
import requests
from app.constants import OrderFeesPence

OPTION_MAP = {
    "standard": {
        "digital": OrderFeesPence.STANDARD_DIGITAL.value,
        "printed": OrderFeesPence.STANDARD_PRINTED.value,
    },
    "full": {
        "digital": OrderFeesPence.FULL_DIGITAL.value,
        "printed": OrderFeesPence.FULL_PRINTED.value,
    },
}

def calculate_delivery_fee(country: str) -> int:
    payload = {
        "A3Colour": 10,
        "Country": country,
        "IsTracking": True
    }

    response = requests.post(
        current_app.config["DELIVERY_FEE_API_URL"],
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code != 200:
        current_app.logger.error(f"Failed to get delivery fee: {response.status_code} - {response.text}")
        raise ValueError("Could not retrieve delivery fee")
    
    response_data = response.json()
    
    return int(response_data) * 100 # Convert pounds to pence


def calculate_amount_based_on_form_data(form_data: dict) -> int:
    processing_option = form_data.get("processing_option")
    amount = 0

    if processing_option not in OPTION_MAP:
        raise ValueError("Invalid processing option")

    amount = OPTION_MAP[processing_option].get(
        form_data.get(
            f"how_do_you_want_your_order_processed_{processing_option}_option"
        )
    )

    if processing_option == "standard" and form_data.get("how_do_you_want_your_order_processed_standard_option") == "printed":
        if country := form_data.get("requester_country"):
            amount += calculate_delivery_fee(country)
        else:
            raise ValueError("Country is required for printed delivery")

    if amount is None:
        raise ValueError("Invalid processing option")

    return amount
