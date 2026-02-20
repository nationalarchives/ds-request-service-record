import io
import os
import uuid

import boto3
from flask import current_app
from werkzeug.datastructures.file_storage import FileStorage


def get_boto3_session() -> boto3.session.Session:
    """
    Returns a boto3 session using the default credential chain.
    When running on AWS infrastructure, this automatically uses IAM roles.
    """
    region = current_app.config.get("AWS_DEFAULT_REGION", "eu-west-2")
    return boto3.session.Session(region_name=region)


def upload_proof_of_death(
    file: FileStorage, session_key: str | None = None
) -> str | None:
    """
    Function that uploads a proof of death file to S3, with a UUID as the filename.
    """

    base_filename = session_key or str(uuid.uuid4())
    holding_prefix = _get_proof_of_death_holding_prefix()
    key_name = _build_key_with_prefix(holding_prefix, base_filename, file.filename)

    if current_app.config.get("ENVIRONMENT_NAME") == "test":
        return key_name

    bucket_name = current_app.config.get("PROOF_OF_DEATH_BUCKET_NAME")

    if not bucket_name:
        current_app.logger.error("Proof of death bucket configuration is missing.")
        return None

    return upload_file_to_s3(
        file=file,
        bucket_name=bucket_name,
        filename_override=key_name,
    )


def upload_file_to_s3(
    file: FileStorage, bucket_name: str, filename_override: str | None = None
) -> str | None:
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

        session = get_boto3_session()
        s3 = session.client("s3")

        filename = file.filename

        if filename_override:
            filename = _build_filename_with_extension(filename_override, file.filename)

        for attempt in range(1, current_app.config["MAX_UPLOAD_ATTEMPTS"] + 1):
            stream = io.BytesIO(data)
            try:
                s3.upload_fileobj(stream, bucket_name, filename)
                return filename
            except Exception as e:
                current_app.logger.error(
                    f"Error uploading file to S3 (attempt {attempt}): {e}"
                )
                if attempt == current_app.config["MAX_UPLOAD_ATTEMPTS"]:
                    current_app.logger.error(
                        f"Max upload attempts reached for file {filename}. Upload failed."
                    )
                    return filename_override  # TODO: Once we have a proper flow for handling failed uploads, we should return None here.
    return filename_override  # TODO: Once we have a proper flow for handling failed uploads, we should return None here.


def move_proof_of_death_to_submitted(key_name: str) -> bool:
    """
    Move a proof of death file from the holding prefix to the submitted prefix.
    """

    if not key_name:
        return False

    if current_app.config.get("ENVIRONMENT_NAME") == "test":
        return True

    bucket_name = current_app.config.get("PROOF_OF_DEATH_BUCKET_NAME")

    if not bucket_name:
        current_app.logger.error("Proof of death bucket configuration is missing.")
        return False

    destination_key = _to_submitted_key(
        key_name,
        holding_prefix=_get_proof_of_death_holding_prefix(),
        submitted_prefix=_get_proof_of_death_submitted_prefix(),
    )

    if destination_key == key_name:
        return True

    session = get_boto3_session()
    s3 = session.client("s3")

    try:
        s3.copy_object(
            Bucket=bucket_name,
            Key=destination_key,
            CopySource={"Bucket": bucket_name, "Key": key_name},
        )
        s3.delete_object(Bucket=bucket_name, Key=key_name)
        return True
    except Exception as e:
        current_app.logger.error(
            f"Error moving proof of death file {key_name} to submitted bucket: {e}"
        )
        return False


def _build_filename_with_extension(base_name: str, original_filename: str) -> str:
    file_extension = os.path.splitext(original_filename)[1]
    existing_extension = os.path.splitext(base_name)[1]
    if existing_extension:
        return base_name
    return f"{base_name}{file_extension}"


def _build_key_with_prefix(prefix: str, base_name: str, original_filename: str) -> str:
    normalized_prefix = _normalize_prefix(prefix)
    filename = _build_filename_with_extension(base_name, original_filename)
    return f"{normalized_prefix}{filename}"


def _normalize_prefix(prefix: str) -> str:
    if not prefix:
        return ""
    return prefix if prefix.endswith("/") else f"{prefix}/"


def _to_submitted_key(
    key_name: str, *, holding_prefix: str, submitted_prefix: str
) -> str:
    normalized_holding = _normalize_prefix(holding_prefix)
    normalized_submitted = _normalize_prefix(submitted_prefix)

    if normalized_holding and key_name.startswith(normalized_holding):
        key_name = key_name[len(normalized_holding) :]

    return f"{normalized_submitted}{key_name}"


def _get_proof_of_death_holding_prefix() -> str:
    return current_app.config.get("PROOF_OF_DEATH_HOLDING_PREFIX")


def _get_proof_of_death_submitted_prefix() -> str:
    return current_app.config.get("PROOF_OF_DEATH_SUBMITTED_PREFIX")


def send_email(to: str, subject: str, body: str) -> bool:
    """
    Function to send an email using AWS SES.
    Return True if email sent successfully, False otherwise.
    """

    session = get_boto3_session()
    ses = session.client("ses")

    try:
        ses.send_email(
            Source=f"{current_app.config['EMAIL_FROM_NAME']} <{current_app.config['EMAIL_FROM']}>",
            Destination={"ToAddresses": [to]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}},
            },
        )
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending email to {to}: {e}")
        return False
