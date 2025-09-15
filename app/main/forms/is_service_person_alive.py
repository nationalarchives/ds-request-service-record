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
from wtforms.validators import InputRequired


class IsServicePersonAlive(FlaskForm):
    content = load_content()

    is_service_person_alive = RadioField(
        get_field_content(content, "is_service_person_alive", "label"),
        choices=[("yes", "Yes"), ("no", "No")],
        validators=[
            InputRequired(
                message=get_field_content(
                    content, "is_service_person_alive", "messages"
                )["required"]
            )
        ],
        widget=TnaRadiosWidget(),
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())
