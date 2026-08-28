import io
import logging
import socket
import uuid
from unittest.mock import patch
from urllib.parse import urlparse

import pytest
from botocore.exceptions import ClientError
from flask import current_app
from werkzeug.datastructures import FileStorage

from app import create_app
from app.lib.aws import (
    get_s3_client,
    move_proof_of_death_to_submitted,
    upload_file_to_s3,
    upload_proof_of_death,
)


def _endpoint_is_reachable(endpoint_url: str) -> bool:
    parsed = urlparse(endpoint_url)
    try:
        with socket.create_connection((parsed.hostname, parsed.port or 80), timeout=3):
            return True
    except OSError:
        return False


@pytest.fixture(scope="module")
def app():
    app = create_app("config.Test")

    endpoint_url = app.config.get("MOCK_S3_ENDPOINT_URL")
    # These tests empty the configured bucket, so refuse to run unless S3 is mocked.
    if (
        not app.config.get("MOCK_S3")
        or not endpoint_url
        or not _endpoint_is_reachable(endpoint_url)
    ):
        pytest.skip(
            "Mock S3 is not reachable. Start it with: docker compose up mock-s3",
            allow_module_level=True,
        )

    return app


@pytest.fixture(scope="module")
def bucket_name(app):
    return app.config["PROOF_OF_DEATH_BUCKET_NAME"]


@pytest.fixture(scope="module")
def s3(app, bucket_name):
    """Creates the configured bucket in the mock S3 if the init container hasn't already."""
    with app.app_context():
        client = get_s3_client()
        try:
            client.head_bucket(Bucket=bucket_name)
        except ClientError:
            client.create_bucket(Bucket=bucket_name)
        try:
            yield client
        finally:
            _empty_bucket(client, bucket_name)


@pytest.fixture()
def context(app, s3, bucket_name):
    """Gives each test an app context and an empty bucket to work against."""
    with app.app_context():
        _empty_bucket(s3, bucket_name)
        yield


def _empty_bucket(client, bucket_name):
    response = client.list_objects_v2(Bucket=bucket_name)
    contents = response.get("Contents", [])
    if contents:
        client.delete_objects(
            Bucket=bucket_name,
            Delete={"Objects": [{"Key": item["Key"]} for item in contents]},
        )


def _list_keys(client, bucket_name) -> list[str]:
    response = client.list_objects_v2(Bucket=bucket_name)
    return sorted(item["Key"] for item in response.get("Contents", []))


def _make_file(
    content=b"some-bytes", filename="original.png", content_type="image/png"
):
    return FileStorage(
        stream=io.BytesIO(content), filename=filename, content_type=content_type
    )


def test_upload_file_to_s3_valid_file_stores_object(context, s3, bucket_name):
    file = _make_file(content=b"some-bytes")

    result = upload_file_to_s3(
        file=file,
        bucket_name=bucket_name,
        filename_override="override-name",
    )

    assert result == "override-name.png"
    assert _list_keys(s3, bucket_name) == ["override-name.png"]

    stored = s3.get_object(Bucket=bucket_name, Key="override-name.png")
    assert stored["Body"].read() == b"some-bytes"
    assert stored["ContentType"] == "image/png"


def test_upload_file_to_s3_pdf_uses_application_pdf_content_type(
    context, s3, bucket_name
):
    file = _make_file(
        content=b"%PDF-1.4\n...",
        filename="death-certificate.pdf",
        content_type="application/octet-stream",
    )

    result = upload_file_to_s3(
        file=file,
        bucket_name=bucket_name,
        filename_override="override-name",
    )

    assert result == "override-name.pdf"

    stored = s3.head_object(Bucket=bucket_name, Key="override-name.pdf")
    assert stored["ContentType"] == "application/pdf"


def test_upload_file_to_s3_uses_original_filename_without_override(
    context, s3, bucket_name
):
    file = _make_file(filename="original.png")

    result = upload_file_to_s3(file=file, bucket_name=bucket_name)

    assert result == "original.png"
    assert _list_keys(s3, bucket_name) == ["original.png"]


def test_upload_file_to_s3_invalid_empty_file_stores_nothing(context, s3, bucket_name):
    file = _make_file(content=b"", filename="empty.png")

    result = upload_file_to_s3(
        file=file,
        bucket_name=bucket_name,
        filename_override="should-not-matter",
    )

    assert result is None
    assert _list_keys(s3, bucket_name) == []


def test_upload_file_to_s3_retries_then_gives_up_on_missing_bucket(context, caplog):
    file = _make_file(filename="test.png")

    with caplog.at_level(logging.ERROR):
        result = upload_file_to_s3(file=file, bucket_name="bucket-that-does-not-exist")

    assert result is None
    attempts = [
        record
        for record in caplog.records
        if "Error uploading file to S3" in record.message
    ]
    assert len(attempts) == 3
    assert "Max upload attempts reached" in caplog.text


def test_upload_proof_of_death_stores_object_under_holding_prefix(
    context, s3, bucket_name
):
    file = _make_file(filename="proof.png")
    generated_uuid = uuid.uuid4()

    with patch("app.lib.aws.uuid.uuid4", return_value=generated_uuid):
        result = upload_proof_of_death(file=file)

    assert result == f"holding/{generated_uuid}.png"
    assert _list_keys(s3, bucket_name) == [f"holding/{generated_uuid}.png"]


def test_move_proof_of_death_to_submitted_copies_and_deletes(context, s3, bucket_name):
    s3.put_object(Bucket=bucket_name, Key="holding/proof.png", Body=b"proof-bytes")

    result = move_proof_of_death_to_submitted("holding/proof.png")

    assert result is True
    assert _list_keys(s3, bucket_name) == ["submitted/proof.png"]

    moved = s3.get_object(Bucket=bucket_name, Key="submitted/proof.png")
    assert moved["Body"].read() == b"proof-bytes"


def test_move_proof_of_death_to_submitted_returns_false_for_missing_object(
    context, s3, bucket_name
):
    result = move_proof_of_death_to_submitted("holding/not-here.png")

    assert result is False
    assert _list_keys(s3, bucket_name) == []


def test_move_proof_of_death_to_submitted_returns_false_when_bucket_not_configured(
    context,
):
    with patch.dict(current_app.config, {"PROOF_OF_DEATH_BUCKET_NAME": ""}):
        assert move_proof_of_death_to_submitted("holding/proof.png") is False


def test_move_proof_of_death_to_submitted_returns_false_without_key(context):
    assert move_proof_of_death_to_submitted("") is False
