from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaSubmitWidget,
)
from wtforms import (
    HiddenField,
    SubmitField,
)


class YourOrderTypeOtherAndDontKnowOfficers(FlaskForm):
    content = load_content()

    processing_option = HiddenField()

    submit = SubmitField(
        get_field_content(
            content,
            "your_order_type_other_and_dont_know_officers",
            "call_to_action",
        ),
        widget=TnaSubmitWidget(),
    )
