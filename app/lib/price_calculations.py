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
    """Calculate delivery fee for printed orders using external API.

    Calls the Record Copying Service API to get delivery costs for
    tracked A3 colour prints to the specified country.

    Args:
        country (str): Destination country name

    Returns:
        int: Delivery fee in pence

    Raises:
        ValueError: If API call fails or returns invalid data
    """
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


def calculate_base_fee(processing_option: str, delivery_type: str) -> int:
    """Calculate base fee for order based on processing option and delivery type.

    Args:
        processing_option (str): Either 'standard' or 'full'
        delivery_type (str): Either 'Digital' or 'PrintedTracked'

    Returns:
        int: Base fee in pence

    Raises:
        ValueError: If invalid processing option or delivery type provided
    """
    if processing_option not in OPTION_MAP:
        raise ValueError("Invalid processing option")

    amount = OPTION_MAP[processing_option].get(delivery_type)

    if amount is None:
        raise ValueError("Invalid delivery type")

    return amount


def calculate_amount_based_on_form_data(form_data: dict) -> int:
    """Calculate total order amount from form data.

    Combines base fee with delivery fee (for printed orders) based on
    processing option, delivery type, and destination country.

    Args:
        form_data (dict): Form data containing processing_option, delivery type, and country

    Returns:
        int: Total amount in pence

    Raises:
        ValueError: If required data is missing or invalid
    """
    delivery_type = get_delivery_type(form_data)
    processing_option = form_data.get("processing_option", "standard")
    amount = calculate_base_fee(processing_option, delivery_type)

    if processing_option == "standard" and delivery_type == "PrintedTracked":
        if country := form_data.get("requester_country"):
            amount += calculate_delivery_fee(country)
        else:
            raise ValueError("Country is required for printed delivery")

    if amount is None:
        raise ValueError("Could not calculate amount")

    return amount


def prepare_order_summary_data(form_data: dict) -> dict:
    """Prepare order summary data for display on the summary page.

    Calculates base fee and delivery fee separately for display purposes.

    Args:
        form_data (dict): Form data containing order details

    Returns:
        dict: Dictionary with processing_option, delivery_type, amount_pence, and delivery_fee_pence
    """
    processing_option = form_data.get("processing_option", "standard")
    delivery_type = get_delivery_type(form_data)

    order_summary_data = {
        "processing_option": processing_option,
        "delivery_type": delivery_type,
        "amount_pence": calculate_base_fee(processing_option, delivery_type),
        "delivery_fee_pence": (
            calculate_delivery_fee(form_data.get("requester_country"))
            if processing_option == "standard" and delivery_type == "PrintedTracked"
            else 0
        ),
    }

    return order_summary_data


def get_delivery_type(form_data: dict) -> str:
    delivery_type = form_data.get("delivery_type")
    if not delivery_type:
        delivery_type = (
            "PrintedTracked" if form_data.get("does_not_have_email") else "Digital"
        )

    return delivery_type
