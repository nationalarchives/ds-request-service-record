from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaRadiosWidget,
    TnaSubmitWidget,
)
from wtforms import (
    RadioField,
    SubmitField,
    HiddenField,
)


class ChooseYourOrderType(FlaskForm):
    content = load_content()

    processing_option = HiddenField()

    submit_standard = SubmitField(
        get_field_content(content, "choose_your_order_type", "standard")[
            "call_to_action"
        ],
        widget=TnaSubmitWidget(),
    )

    submit_full_check = SubmitField(
        get_field_content(content, "choose_your_order_type", "full_check")[
            "call_to_action"
        ],
        widget=TnaSubmitWidget(),
    )
