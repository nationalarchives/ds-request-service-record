from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaCheckboxWidget,
    TnaSubmitWidget,
)
from wtforms import (
    BooleanField,
    SubmitField,
)
from wtforms.validators import InputRequired


class BeforeYouStart(FlaskForm):
    content = load_content()

    ready_to_continue = BooleanField(
        get_field_content(content, "ready_to_continue", "label"),
        widget=TnaCheckboxWidget(),
        validators=[
            InputRequired(
                message=get_field_content(content, "ready_to_continue", "messages")[
                    "required"
                ]
            )
        ],
    )

    submit = SubmitField(
        get_field_content(content, "before_you_start", "call_to_action"),
        widget=TnaSubmitWidget(),
    )
