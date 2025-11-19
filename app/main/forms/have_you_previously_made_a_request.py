from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaSubmitWidget,
    TnaTextInputWidget,
)
from wtforms import (
    StringField,
    SubmitField,
)


class HaveYouPreviouslyMadeARequest(FlaskForm):
    content = load_content()

    mod_reference = StringField(
        get_field_content(content, "have_you_previously_made_a_request", "mod_reference")[
            "label"
        ],
        description=get_field_content(
            content, "have_you_previously_made_a_request", "mod_reference"
        )["hint_text"],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    case_reference_number = StringField(
        get_field_content(content, "have_you_previously_made_a_request", "case_reference_number")[
            "label"
        ],
        description=get_field_content(
            content, "have_you_previously_made_a_request", "case_reference_number"
        )["hint_text"],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    submit = SubmitField(
        get_field_content(
            content, "have_you_previously_made_a_request", "call_to_action"
        ),
        widget=TnaSubmitWidget(),
    )
