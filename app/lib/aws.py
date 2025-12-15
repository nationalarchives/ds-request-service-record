"""
AWS integration module.

This module handles AWS service interactions including S3 file uploads
and SES email sending.
"""

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


def upload_proof_of_death(file: FileStorage) -> str | None:
    """
    Upload a proof of death file to S3 with a UUID as the filename.
    
    In test environment, returns UUID without uploading to S3.
    
    Args:
        file: File to upload.
        
    Returns:
        str: UUID filename if successful, None otherwise.
    """
    uuid_filename = str(uuid.uuid4())

    if current_app.config.get("ENVIRONMENT_NAME") == "test":
        return uuid_filename

    return upload_file_to_s3(
        file=file,
        bucket_name=current_app.config["PROOF_OF_DEATH_BUCKET_NAME"],
        filename_override=uuid_filename,
    )


def upload_file_to_s3(
    file: FileStorage, 
    bucket_name: str, 
    filename_override: str | None = None
) -> str | None:
    """
    Upload a file to a specified S3 bucket with retry logic.
    
    The file content is read into memory to allow for:
    - Empty file validation
    - Multiple retry attempts without re-opening the file
    
    Args:
        file: File to upload.
        bucket_name: Name of the S3 bucket.
        filename_override: Optional custom filename (extension will be preserved).
        
    Returns:
        str: Filename or override if successful, None if file is empty.
        
    Note:
        Currently returns filename_override even on upload failure to prevent
        blocking user flow. This should be changed to return None once proper
        error handling flow is implemented.
    """
    if not file:
        return filename_override

    data = file.read()

    if not data:
        current_app.logger.error("File is empty, cannot upload to S3.")
        return None

    session = get_boto3_session()
    s3 = session.client("s3")

    filename = file.filename

    if filename_override:
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{filename_override}{file_extension}"

    max_attempts = current_app.config["MAX_UPLOAD_ATTEMPTS"]
    
    for attempt in range(1, max_attempts + 1):
        stream = io.BytesIO(data)
        try:
            s3.upload_fileobj(stream, bucket_name, filename)
            current_app.logger.info(f"Successfully uploaded {filename} to S3")
            return filename_override
        except Exception as e:
            current_app.logger.error(
                f"Error uploading file to S3 (attempt {attempt}/{max_attempts}): {e}"
            )
            if attempt == max_attempts:
                current_app.logger.error(
                    f"Max upload attempts reached for file {filename}. Upload failed."
                )
                # TODO: Return None here once proper error handling flow exists
                return filename_override
    
    # TODO: Return None here once proper error handling flow exists
    return filename_override


def send_email(to: str, subject: str, body: str) -> None:
    """
    Send an email using AWS SES.
    
    Args:
        to: Recipient email address.
        subject: Email subject line.
        body: Email body text.
        
    Raises:
        Exception: If email sending fails (propagated from boto3).
    """
    session = get_boto3_session()
    ses = session.client("ses")

    try:
        ses.send_email(
            Source=current_app.config["EMAIL_FROM"],
            Destination={"ToAddresses": [to]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}},
            },
        )
        current_app.logger.info(f"Email sent successfully to {to}")
    except Exception as e:
        current_app.logger.error(f"Failed to send email to {to}: {e}")
        raise
