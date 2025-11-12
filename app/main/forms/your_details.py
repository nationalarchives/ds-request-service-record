from app.lib.content import get_field_content, load_content
from app.main.forms.validation_helpers.field_required_unless_checkbox_checked import (
    field_required_unless_checkbox_checked,
)
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaCheckboxWidget,
    TnaSubmitWidget,
    TnaTextInputWidget,
)
from wtforms import (
    BooleanField,
    EmailField,
    StringField,
    SubmitField,
)
from wtforms.validators import Email, InputRequired


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
            field_required_unless_checkbox_checked(
                "does_not_have_email",
                message=get_field_content(content, "requester_email", "messages")[
                    "required"
                ],
            ),
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
        description=get_field_content(content, "does_not_have_email", "description"),
        widget=TnaCheckboxWidget(),
        validators=[],
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())
