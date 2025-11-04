from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import TnaRadiosWidget, TnaSubmitWidget
from wtforms import RadioField, SubmitField
from wtforms.validators import InputRequired


class WasServicePersonAnOfficer(FlaskForm):
    content = load_content()

    were_they_a_commissioned_officer = RadioField(
        get_field_content(content, "were_they_a_commissioned_officer", "label"),
        choices=[("yes", "Yes"), ("no", "No"), ("unknown", "I don't know")],
        validators=[
            InputRequired(
                message=get_field_content(
                    content, "were_they_a_commissioned_officer", "messages"
                )["required"]
            )
        ],
        widget=TnaRadiosWidget(),
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())
