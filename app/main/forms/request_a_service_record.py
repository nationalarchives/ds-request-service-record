from app.constants import COUNTRY_CHOICES, ServiceBranches
from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from tna_frontend_jinja.wtforms import (
    TnaDateField,
    TnaDroppableFileInputWidget,
    TnaRadiosWidget,
    TnaSelectWidget,
    TnaSubmitWidget,
    TnaTextareaWidget,
    TnaTextInputWidget,
)
from tna_frontend_jinja.wtforms import validators as tna_frontend_validators
from wtforms import (
    EmailField,
    FileField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import Email, InputRequired, Optional


class RequestAServiceRecord(FlaskForm):
    content = load_content()

    forenames = StringField(
        get_field_content(content, "forenames", "label"),
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(
                message=get_field_content(content, "forenames", "messages")["required"]
            ),
        ],
    )

    lastname = StringField(
        get_field_content(content, "last_name", "label"),
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(
                message=get_field_content(content, "last_name", "messages")["required"]
            ),
        ],
    )

    other_last_names = StringField(
        get_field_content(content, "other_last_names", "label"),
        widget=TnaTextInputWidget(),
        validators=[],
    )

    date_of_birth = TnaDateField(
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

    place_of_birth = StringField(
        get_field_content(content, "place_of_birth", "label"),
        widget=TnaTextInputWidget(),
        validators=[],
    )

    date_of_death = TnaDateField(
        get_field_content(content, "date_of_death", "label"),
        description=get_field_content(content, "date_of_death", "description"),
        validators=[
            Optional(),
            tna_frontend_validators.PastDate(
                message=get_field_content(content, "date_of_death", "messages")[
                    "past_date"
                ],
                include_now=True,
            ),
        ],
    )

    service_number = StringField(
        get_field_content(content, "service_number", "label"),
        widget=TnaTextInputWidget(),
        validators=[],
    )

    regiment = StringField(
        get_field_content(content, "regiment", "label"),
        widget=TnaTextInputWidget(),
        validators=[],
    )

    service_branch = RadioField(
        get_field_content(content, "service_branch", "label"),
        choices=[
            (name, member.value) for name, member in ServiceBranches.__members__.items()
        ],
        validators=[
            InputRequired(
                message=get_field_content(content, "service_branch", "messages")[
                    "required"
                ]
            )
        ],
        widget=TnaRadiosWidget(),
    )

    mod_reference = StringField(
        get_field_content(content, "mod_reference", "label"),
        description=get_field_content(content, "mod_reference", "description"),
        widget=TnaTextInputWidget(),
        validators=[],
    )

    additional_information = TextAreaField(
        get_field_content(content, "additional_information", "label"),
        description=get_field_content(content, "additional_information", "description"),
        validators=[],
        widget=TnaTextareaWidget(),
    )

    evidence_of_death = FileField(
        get_field_content(content, "evidence_of_death", "label"),
        validators=[
            FileAllowed(
                upload_set=["jpg", "png", "gif"],
                message=get_field_content(content, "evidence_of_death", "messages")[
                    "file_allowed"
                ],
            ),
            FileSize(
                max_size=20 * 1024 * 1024,
                message=get_field_content(content, "evidence_of_death", "messages")[
                    "file_size"
                ],
            ),
        ],
        widget=TnaDroppableFileInputWidget(),
    )

    died_in_service = RadioField(
        get_field_content(content, "died_in_service", "label"),
        choices=[("yes", "Yes"), ("no", "No"), ("unknown", "Unknown")],
        validators=[
            InputRequired(
                message=get_field_content(content, "died_in_service", "messages")[
                    "required"
                ]
            )
        ],
        widget=TnaRadiosWidget(),
    )

    case_reference_number = StringField(
        get_field_content(content, "case_reference_number", "label"),
        description=get_field_content(content, "case_reference_number", "description"),
        widget=TnaTextInputWidget(),
        validators=[],
    )

    requester_title = StringField(
        get_field_content(content, "requester_title", "label"),
        widget=TnaTextInputWidget(),
        validators=[],
    )

    requester_first_name = StringField(
        get_field_content(content, "requester_first_name", "label"),
        widget=TnaTextInputWidget(),
        validators=[],
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

    requester_contact_preference = RadioField(
        get_field_content(content, "contact_preferences", "label"),
        choices=[("email", "Email"), ("post", "Post")],
        validators=[
            InputRequired(
                message=get_field_content(content, "contact_preferences", "messages")[
                    "required"
                ]
            )
        ],
        widget=TnaRadiosWidget(),
    )

    requester_email = EmailField(
        get_field_content(content, "requester_email", "label"),
        validators=[
            InputRequired(
                message=get_field_content(content, "requester_email", "messages")[
                    "required"
                ]
            ),
            Email(
                message=get_field_content(content, "requester_email", "messages")[
                    "address_format"
                ]
            ),
        ],
        widget=TnaTextInputWidget(),
    )

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
        ]
        + COUNTRY_CHOICES,
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
