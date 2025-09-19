from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaDateField,
    TnaRadiosWidget,
    TnaSubmitWidget,
    TnaTextareaWidget,
    TnaTextInputWidget,
)
from tna_frontend_jinja.wtforms import validators as tna_frontend_validators
from wtforms import (
    RadioField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import InputRequired


class ServicePersonDetails(FlaskForm):
    content = load_content()

    first_name = StringField(
        get_field_content(content, "first_name", "label"),
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(
                message=get_field_content(content, "first_name", "messages")["required"]
            ),
        ],
    )

    middle_names = StringField(
        get_field_content(content, "middle_names", "label"),
        widget=TnaTextInputWidget(),
        validators=[],
    )

    last_name = StringField(
        get_field_content(content, "last_name", "label"),
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(
                message=get_field_content(content, "last_name", "messages")["required"]
            )
        ],
    )

    place_of_birth = StringField(
        get_field_content(content, "place_of_birth", "label"),
        widget=TnaTextInputWidget(),
        validators=[],
    )

    date_of_death = TnaDateField(
        get_field_content(content, "date_of_death", "label"),
        description=get_field_content(content, "date_of_death", "description"),
        validators=[
            tna_frontend_validators.PastDate(
                message=get_field_content(content, "date_of_death", "messages")[
                    "past_date"
                ],
                include_today=True,
            ),
        ],
    )

    died_in_service = RadioField(
        get_field_content(content, "died_in_service", "label"),
        choices=[("yes", "Yes"), ("no", "No"), ("dont_know", "Don't know")],
        validators=[],
        widget=TnaRadiosWidget(),
        validate_choice=False,
    )

    service_number = StringField(
        get_field_content(content, "service_number", "label"),
        widget=TnaTextInputWidget(),
        validators=[],
    )

    regiment = StringField(
        get_field_content(content, "regiment", "label"),
        widget=TnaTextInputWidget(),
        validators=[],
    )

    additional_information = TextAreaField(
        get_field_content(content, "additional_information", "label"),
        description=get_field_content(content, "additional_information", "description"),
        validators=[],
        widget=TnaTextareaWidget(),
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())
