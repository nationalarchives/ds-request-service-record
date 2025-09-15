from app.lib.content import get_field_content, load_content
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

    what_was_their_date_of_birth = TnaDateField(
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
        ],
    )

    submit = SubmitField(
        get_field_content(content, "date_of_birth", "call_to_action"),
        widget=TnaSubmitWidget(),
    )
