from app.lib.content import get_field_content, load_content
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from tna_frontend_jinja.wtforms import TnaDroppableFileInputWidget, TnaSubmitWidget
from wtforms import (
    FileField,
    SubmitField,
)


class UploadAProofOfDeath(FlaskForm):
    content = load_content()

    proof_of_death = FileField(
        get_field_content(content, "upload_a_proof_of_death", "label"),
        validators=[
            FileAllowed(
                upload_set=["jpg", "png", "gif"],
                message=get_field_content(
                    content, "upload_a_proof_of_death", "messages"
                )["file_allowed"],
            ),
            FileSize(
                max_size=5 * 1024 * 1024,
                message=get_field_content(
                    content, "upload_a_proof_of_death", "messages"
                )["file_size"],
            ),
        ],
        widget=TnaDroppableFileInputWidget(),
    )

    submit = SubmitField(
        get_field_content(content, "upload_a_proof_of_death", "call_to_action"),
        widget=TnaSubmitWidget(),
    )
