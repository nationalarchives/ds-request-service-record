from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaCheckboxWidget,
    TnaSubmitWidget,
    TnaTextInputWidget,
)
from tna_frontend_jinja.wtforms import validators as tna_frontend_validators
from wtforms import (
    EmailField,
    StringField,
    SubmitField,
    BooleanField,
)
from wtforms.validators import Email, InputRequired, Optional


class YourDetails(FlaskForm):
    content = load_content()

    requester_first_name = StringField(
        get_field_content(content, "requester_first_name", "label"),
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(
                message=get_field_content(content, "requester_first_name", "messages")[
                    "required"
                ]
            )
        ],
    )

    requester_last_name = StringField(
        get_field_content(content, "requester_last_name", "label"),
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(
                message=get_field_content(content, "requester_last_name", "messages")[
                    "required"
                ]
            )
        ],
    )

    requester_email = EmailField(
        get_field_content(content, "requester_email", "label"),
        validators=[
            Optional(),
            Email(
                message=get_field_content(content, "requester_email", "messages")[
                    "address_format"
                ]
            ),
        ],
        widget=TnaTextInputWidget(),
    )

    does_not_have_email = BooleanField(
        get_field_content(content, "does_not_have_email", "label"),
        widget=TnaCheckboxWidget(),
        validators=[],
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())
