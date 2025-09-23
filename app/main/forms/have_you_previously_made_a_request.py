from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaSubmitWidget,
    TnaTextInputWidget,
)
from tna_frontend_jinja.wtforms import validators as tna_frontend_validators
from wtforms import (
    StringField,
    SubmitField,
)
from wtforms.validators import Email, InputRequired


class HaveYouPreviouslyMadeARequest(FlaskForm):
    content = load_content()

    with_mod = StringField(
        get_field_content(content, "have_you_previously_made_a_request", "with_mod")[
            "label"
        ],
        description=get_field_content(
            content, "have_you_previously_made_a_request", "with_mod"
        )["hint_text"],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    with_tna = StringField(
        get_field_content(content, "have_you_previously_made_a_request", "with_tna")[
            "label"
        ],
        description=get_field_content(
            content, "have_you_previously_made_a_request", "with_tna"
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
