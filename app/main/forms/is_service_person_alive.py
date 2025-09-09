from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from tna_frontend_jinja.wtforms import (
    TnaRadiosWidget,
    TnaSubmitWidget,
)
from tna_frontend_jinja.wtforms import validators as tna_frontend_validators
from wtforms import (
    RadioField,
    SubmitField,
)
from wtforms.validators import Email, InputRequired


class IsServicePersonAlive(FlaskForm):
    content = load_content()

    is_service_person_alive = RadioField(
        get_field_content(content, "is_service_person_alive", "label"),
        choices=[("yes", "Yes"), ("no", "No")],
        validators=[
            InputRequired(
                message=get_field_content(content, "is_service_person_alive", "messages")[
                    "required"
                ]
            )
        ],
        widget=TnaRadiosWidget(),
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())
