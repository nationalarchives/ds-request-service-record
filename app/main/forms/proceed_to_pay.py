from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaSubmitWidget,
)
from wtforms import (
    SubmitField,
)

from app.lib.content import get_field_content, load_content


class ProceedToPay(FlaskForm):
    content = load_content()

    submit = SubmitField(
        get_field_content(content, "proceed_to_payment", "call_to_action"),
        widget=TnaSubmitWidget(),
    )
