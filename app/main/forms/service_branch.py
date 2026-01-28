from app.constants import ServiceBranches
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


class ServiceBranch(FlaskForm):
    content = load_content()

    service_branch = RadioField(
        "",
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
        render_kw={"label": ""},
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())
