from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from tna_frontend_jinja.wtforms import TnaRadiosWidget, TnaSubmitWidget
from app.lib.content import get_field_content, load_content
from wtforms.validators import InputRequired


class WasServicePersonAnOfficer(FlaskForm):
    content = load_content()

    was_service_person_an_officer = RadioField(
        get_field_content(content, "was_service_person_an_officer", "label"),
        choices=[("yes", "Yes"), ("no", "No"), ("unknown", "I don't know")],
        validators=[
            InputRequired(
                message=get_field_content(content, "was_service_person_an_officer", "messages")[
                    "required"
                ]
            )
        ],
        widget=TnaRadiosWidget(),
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())

