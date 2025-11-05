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

    if processing_option == "standard":
        if (
            form_data.get("how_do_you_want_your_order_processed_standard_option")
            == "digital"
        ):
            amount = OrderFeesPence.STANDARD_DIGITAL.value
        else:
            # TODO: Will add delivery price if "standard printed" is chosen as part of FOI-128, from MOD Copying API
            amount = OrderFeesPence.STANDARD_PRINTED.value
    if processing_option == "full":
        if (
            form_data.get("how_do_you_want_your_order_processed_full_option")
            == "digital"
        ):
            amount = OrderFeesPence.FULL_DIGITAL.value
        else:
            amount = OrderFeesPence.FULL_PRINTED.value
    return amount
