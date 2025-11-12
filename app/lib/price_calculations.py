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


def calculate_amount_based_on_form_data(form_data):
    processing_option = form_data.get("processing_option")
    amount = 0

    if processing_option not in OPTION_MAP:
        raise ValueError("Invalid processing option")

    amount = OPTION_MAP[processing_option].get(
        form_data.get(
            f"how_do_you_want_your_order_processed_{processing_option}_option"
        )
    )

    if amount is None:
        raise ValueError("Invalid processing option")

    return amount
