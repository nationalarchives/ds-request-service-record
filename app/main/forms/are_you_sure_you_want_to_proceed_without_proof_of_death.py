from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import TnaRadiosWidget, TnaSubmitWidget
from wtforms import RadioField, SubmitField
from wtforms.validators import InputRequired


class AreYouSureYouWantToProceedWithoutProofOfDeath(FlaskForm):
    content = load_content()

    are_you_sure_you_want_to_proceed_without_proof_of_death = RadioField(
        get_field_content(
            content, "are_you_sure_you_want_to_proceed_without_proof_of_death", "label"
        ),
        choices=[
            (
                "yes",
                get_field_content(
                    content,
                    "are_you_sure_you_want_to_proceed_without_proof_of_death",
                    "options",
                )["yes"],
            ),
            (
                "no",
                get_field_content(
                    content,
                    "are_you_sure_you_want_to_proceed_without_proof_of_death",
                    "options",
                )["no"],
            ),
        ],
        validators=[
            InputRequired(
                message=get_field_content(
                    content,
                    "are_you_sure_you_want_to_proceed_without_proof_of_death",
                    "messages",
                )["required"]
            )
        ],
        widget=TnaRadiosWidget(),
    )

    submit = SubmitField(
        get_field_content(
            content,
            "are_you_sure_you_want_to_proceed_without_proof_of_death",
            "call_to_action",
        ),
        widget=TnaSubmitWidget(),
    )
