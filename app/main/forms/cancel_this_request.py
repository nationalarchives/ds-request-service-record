from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaSubmitWidget,
)
from wtforms import (
    SubmitField,
)


class CancelThisRequest(FlaskForm):
    content = load_content()

    submit = SubmitField(
        get_field_content(content, "cancel_this_request", "call_to_action"),
        widget=TnaSubmitWidget(),
    )
