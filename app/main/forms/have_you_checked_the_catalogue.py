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


class HaveYouCheckedTheCatalogue(FlaskForm):
    content = load_content()

    have_you_checked_the_catalogue = RadioField(
        content["pages"]["have_you_checked_the_catalogue"]["heading"],
        choices=[("yes", "Yes"), ("no", "No")],
        validators=[
            InputRequired(
                message=get_field_content(
                    content, "have_you_checked_the_catalogue", "messages"
                )["required"]
            )
        ],
        widget=TnaRadiosWidget(),
        render_kw={"label": ""},
    )

    submit = SubmitField(
        get_field_content(content, "have_you_checked_the_catalogue", "call_to_action"),
        widget=TnaSubmitWidget(),
    )
