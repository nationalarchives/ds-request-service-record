import boto3
import uuid
import os
import io

from flask import current_app
from werkzeug.datastructures.file_storage import FileStorage


def upload_proof_of_death(file: FileStorage) -> str | None:
    """
    Function that uploads a proof of death file to S3, with a UUID as the filename.
    """

    uuid_filename = str(uuid.uuid4())

    return upload_file_to_s3(file=file, bucket_name=current_app.config["PROOF_OF_DEATH_BUCKET_NAME"], filename_override=uuid_filename)


def upload_file_to_s3(file: FileStorage, bucket_name: str, filename_override: str | None = None) -> str | None:
    """
    Generic function that takes a file and uploads it to a given S3 bucket.

    We read the file into a variable so that we can check if it's empty, and also to allow for retries
    otherwise the file gets closed and we can't re-read it.

    Returns file name for use in other parts of application.
    """
    if file:
        data = file.read()

        if not data:
            current_app.logger.error("File is empty, cannot upload to S3.")
            return None
        
        s3 = boto3.client(
            "s3",
            aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
            aws_session_token=current_app.config.get("AWS_SESSION_TOKEN"),
            region_name=current_app.config.get("AWS_DEFAULT_REGION", "eu-west-2"),
        )

        filename = file.filename

        if filename_override:
            file_extension = os.path.splitext(file.filename)[1]
            filename = f"{filename_override}{file_extension}"

        for attempt in range(1, current_app.config["MAX_UPLOAD_ATTEMPTS"] + 1):
            stream = io.BytesIO(data)
            try:
                s3.upload_fileobj(stream, bucket_name, filename)
                return filename
            except Exception as e:
                current_app.logger.error(f"Error uploading file to S3 (attempt {attempt}): {e}")
                if attempt == current_app.config["MAX_UPLOAD_ATTEMPTS"]:
                    current_app.logger.error(f"Max upload attempts reached for file {filename}. Upload failed.")
                    return None

        return filename
    return None

def send_email(to: str, subject: str, body: str) -> None:
    """
    Function to send an email using AWS SES.
    """
    ses = boto3.client(
        "ses",
        aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
        region_name=current_app.config.get("AWS_DEFAULT_REGION", "eu-west-2"),
    )

    try:
        ses.send_email(
            Source=current_app.config["EMAIL_FROM"],
            Destination={"ToAddresses": [to]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}},
            },
        )
    except Exception as e:
        current_app.logger.error(f"Error sending email: {e}")