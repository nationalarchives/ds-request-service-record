from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import TnaRadiosWidget, TnaSubmitWidget
from wtforms import RadioField, SubmitField
from wtforms.validators import InputRequired


class DoYouHaveAProofOfDeath(FlaskForm):
    content = load_content()

    do_you_have_a_proof_of_death = RadioField(
        get_field_content(content, "do_you_have_a_proof_of_death", "label"),
        choices=[("yes", "Yes"), ("no", "No")],
        validators=[
            InputRequired(
                message=get_field_content(
                    content, "do_you_have_a_proof_of_death", "messages"
                )["required"]
            )
        ],
        widget=TnaRadiosWidget(),
    )

    submit = SubmitField(
        get_field_content(content, "do_you_have_a_proof_of_death", "call_to_action"),
        widget=TnaSubmitWidget(),
    )
