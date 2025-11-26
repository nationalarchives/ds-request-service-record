from app.constants import get_country_choices
from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaSelectWidget,
    TnaSubmitWidget,
    TnaTextInputWidget,
)
from wtforms import (
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired


class YourPostalAddress(FlaskForm):
    content = load_content()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requester_country.choices += get_country_choices()

    requester_address1 = StringField(
        get_field_content(content, "requester_address_line_1", "label"),
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(
                message=get_field_content(
                    content, "requester_address_line_1", "messages"
                )["required"]
            )
        ],
    )

    requester_address2 = StringField(
        get_field_content(content, "requester_address_line_2", "label"),
        widget=TnaTextInputWidget(),
        validators=[],
    )

    requester_town_city = StringField(
        get_field_content(content, "requester_town_city", "label"),
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(
                message=get_field_content(content, "requester_town_city", "messages")[
                    "required"
                ]
            )
        ],
    )

    requester_county = StringField(
        get_field_content(content, "requester_county", "label"),
        widget=TnaTextInputWidget(),
        validators=[],
    )

    requester_postcode = StringField(
        get_field_content(content, "requester_postcode", "label"),
        widget=TnaTextInputWidget(),
        validators=[],
    )

    requester_country = SelectField(
        get_field_content(content, "requester_country", "label"),
        choices=[
            get_field_content(content, "requester_country", "prompt_to_select"),
        ],
        widget=TnaSelectWidget(),
        validators=[
            InputRequired(
                message=get_field_content(content, "requester_country", "messages")[
                    "required"
                ]
            )
        ],
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())
