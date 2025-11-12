import io
from unittest.mock import MagicMock, patch

import pytest
from app.lib.aws import upload_file_to_s3
from werkzeug.datastructures import FileStorage

from app import create_app


@pytest.fixture(scope="module")
def app():
    app = create_app("config.Test")
    # Minimal config needed by upload_file_to_s3
    app.config.update(
        {
            "AWS_ACCESS_KEY_ID": "test",
            "AWS_SECRET_ACCESS_KEY": "test",
            "AWS_SESSION_TOKEN": "test-token",
            "AWS_DEFAULT_REGION": "eu-west-2",
            "MAX_UPLOAD_ATTEMPTS": 3,
        }
    )
    return app


@pytest.fixture()
def context(app):
    with app.app_context():
        yield


def test_upload_file_to_s3_valid_file_returns_filename(context):
    # Arrange: create a non-empty file-like object
    content = b"some-bytes"
    stream = io.BytesIO(content)
    fs = FileStorage(stream=stream, filename="original.png", content_type="image/png")

    mock_s3 = MagicMock()
    # Simulate successful upload
    mock_s3.upload_fileobj.return_value = None

    with patch("app.lib.aws.boto3.client", return_value=mock_s3) as mock_client:
        result = upload_file_to_s3(
            file=fs,
            bucket_name="test-bucket",
            filename_override="override-name",
        )

    assert isinstance(result, str)
    assert result == "override-name"
    mock_client.assert_called_once_with(
        "s3",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        aws_session_token="test-token",
        region_name="eu-west-2",
    )
    mock_s3.upload_fileobj.assert_called_once()


def test_upload_file_to_s3_invalid_empty_file_returns_none(context):
    # Arrange: empty file (read() -> b'')
    empty_stream = io.BytesIO(b"")
    fs = FileStorage(
        stream=empty_stream, filename="empty.png", content_type="image/png"
    )

    # Because the function returns early for empty content, boto3 should never be called
    with patch("app.lib.aws.boto3.client") as mock_client:
        result = upload_file_to_s3(
            file=fs,
            bucket_name="test-bucket",
            filename_override="should-not-matter",
        )

    assert result is None
    mock_client.assert_not_called()
