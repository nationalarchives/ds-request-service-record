from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaSubmitWidget,
)
from wtforms import (
    SubmitField,
)


class WeAreUnlikelyToHoldThisRecord(FlaskForm):
    content = load_content()

    submit = SubmitField(
        get_field_content(
            content, "we_are_unlikely_to_hold_this_record", "call_to_action"
        ),
        widget=TnaSubmitWidget(),
    )
