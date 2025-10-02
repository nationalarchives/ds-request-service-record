from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaRadiosWidget,
    TnaSubmitWidget,
)
from wtforms import (
    RadioField,
    SubmitField,
)

from app.main.forms.validation_helpers.radio_conditionally_required import (
    radio_conditionally_required,
)


class HowDoYouWantYourOrderProcessed(FlaskForm):
    content = load_content()

    # This field is not exposed to the user. It is used to determine which option the form
    # is relevant to (standard or full) for validation purposes. For example, if the user has submitted
    # the standard option, the standard radio field is required, but the full option is not.
    processing_option = RadioField(
        "",
        choices=["standard", "full"],
        validators=[],
        validate_choice=False,
    )

    how_do_you_want_your_order_processed_standard_option = RadioField(
        get_field_content(content, "how_do_you_want_your_order_processed", "label"),
        choices=[
            (
                "digital",
                get_field_content(
                    content, "how_do_you_want_your_order_processed", "standard"
                )["digital"],
            ),
            (
                "printed",
                get_field_content(
                    content, "how_do_you_want_your_order_processed", "standard"
                )["printed"],
            ),
        ],
        validators=[
            radio_conditionally_required(
                other_field_name="processing_option",
                other_field_value="standard",
                message=get_field_content(
                    content, "how_do_you_want_your_order_processed", "messages"
                )["no_radio_selected"],
            )
        ],
        validate_choice=False,
        widget=TnaRadiosWidget(),
    )

    how_do_you_want_your_order_processed_full_option = RadioField(
        get_field_content(content, "how_do_you_want_your_order_processed", "label"),
        choices=[
            (
                "digital",
                get_field_content(
                    content, "how_do_you_want_your_order_processed", "full"
                )["digital"],
            ),
            (
                "printed",
                get_field_content(
                    content, "how_do_you_want_your_order_processed", "full"
                )["printed"],
            ),
        ],
        validators=[
            radio_conditionally_required(
                other_field_name="processing_option",
                other_field_value="full",
                message=get_field_content(
                    content, "how_do_you_want_your_order_processed", "messages"
                )["no_radio_selected"],
            )
        ],
        validate_choice=False,
        widget=TnaRadiosWidget(),
    )

    submit_standard = SubmitField(
        get_field_content(content, "how_do_you_want_your_order_processed", "standard")[
            "continue"
        ],
        widget=TnaSubmitWidget(),
    )
    submit_full_check = SubmitField(
        get_field_content(content, "how_do_you_want_your_order_processed", "full")[
            "continue"
        ],
        widget=TnaSubmitWidget(),
    )
