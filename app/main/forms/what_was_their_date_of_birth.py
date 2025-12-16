from app.lib.content import get_field_content, load_content
from app.main.forms.validation_helpers.born_too_early import BornTooEarly
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaDateField,
    TnaSubmitWidget,
)
from tna_frontend_jinja.wtforms import validators as tna_frontend_validators
from wtforms import (
    SubmitField,
)
from wtforms.validators import InputRequired


class WhatWasTheirDateOfBirth(FlaskForm):
    content = load_content()

    date_of_birth = TnaDateField(
        get_field_content(content, "date_of_birth", "label"),
        description=get_field_content(content, "date_of_birth", "description"),
        validators=[
            InputRequired(
                message=get_field_content(content, "date_of_birth", "messages")[
                    "required"
                ]
            ),
            tna_frontend_validators.PastDate(
                message=get_field_content(content, "date_of_birth", "messages")[
                    "past_date"
                ]
            ),
            BornTooEarly(
                message=get_field_content(content, "date_of_birth", "messages")[
                    "born_too_early"
                ]
            ),
        ],
    )

    submit = SubmitField(
        get_field_content(content, "date_of_birth", "call_to_action"),
        widget=TnaSubmitWidget(),
    )
