from app.lib.content import get_field_content, load_content
from app.main.forms.validation_helpers.text_field_conditionally_required import (
    text_field_required_unless_radio_has_specific_selection,
)
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaRadiosWidget,
    TnaSubmitWidget,
    TnaTextInputWidget,
)
from wtforms import (
    RadioField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired


class HaveYouPreviouslyMadeARequest(FlaskForm):
    content = load_content()

    have_you_previously_made_a_request = RadioField(
        get_field_content(content, "have_you_previously_made_a_request", "label"),
        choices=[
            (
                "yes_mod",
                get_field_content(
                    content, "have_you_previously_made_a_request", "options"
                )["yes_mod"],
            ),
            (
                "yes_tna",
                get_field_content(
                    content, "have_you_previously_made_a_request", "options"
                )["yes_tna"],
            ),
            (
                "no",
                get_field_content(
                    content, "have_you_previously_made_a_request", "options"
                )["no"],
            ),
        ],
        validators=[
            InputRequired(
                message=get_field_content(
                    content, "have_you_previously_made_a_request", "messages"
                )["required"]
            )
        ],
        widget=TnaRadiosWidget(),
    )

    case_reference_number = StringField(
        get_field_content(
            content, "have_you_previously_made_a_request", "case_reference_number"
        )["label"],
        description=get_field_content(
            content, "have_you_previously_made_a_request", "case_reference_number"
        )["hint_text"],
        widget=TnaTextInputWidget(),
        validators=[
            text_field_required_unless_radio_has_specific_selection(
                radio_field_name="have_you_previously_made_a_request",
                permissible_selection="no",
                message=get_field_content(
                    content, "have_you_previously_made_a_request", "messages"
                )["reference_number_required"],
            )
        ],
    )

    submit = SubmitField(
        get_field_content(
            content, "have_you_previously_made_a_request", "call_to_action"
        ),
        widget=TnaSubmitWidget(),
    )
