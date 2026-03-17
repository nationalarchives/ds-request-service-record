from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaSubmitWidget,
)
from wtforms import (
    SubmitField,
)


class SorryYouWillHaveToStartAgain(FlaskForm):
    content = load_content()

    submit = SubmitField(
        get_field_content(
            content, "sorry_you_will_have_to_start_again", "call_to_action"
        ),
        widget=TnaSubmitWidget(),
    )
