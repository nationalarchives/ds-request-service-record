from app.constants import ServiceBranches
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


class ServiceBranch(FlaskForm):
    content = load_content()

    service_branch = RadioField(
        get_field_content(content, "service_branch", "label"),
        choices=[
            (name, member.value) for name, member in ServiceBranches.__members__.items()
        ],
        validators=[
            InputRequired(
                message=get_field_content(content, "service_branch", "messages")[
                    "required"
                ]
            )
        ],
        widget=TnaRadiosWidget(),
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())
