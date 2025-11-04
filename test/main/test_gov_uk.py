from unittest.mock import MagicMock, patch

import pytest
from app.lib.gov_uk_pay import (
    create_payment,
    validate_payment,
)

from app import create_app


@pytest.fixture(scope="module")
def test_app():
    app = create_app("config.Test")
    with app.app_context():
        yield app


@patch("app.lib.gov_uk_pay.requests.post")
def test_create_payment_success(mock_post, test_app):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "payment_id": "abc123",
        "_links": {"next_url": {"href": "http://pay"}},
    }
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    with test_app.app_context():
        result = create_payment(1000, "desc", "ref", "test@email.com", "http://return")
        assert result["payment_id"] == "abc123"
        assert result["_links"]["next_url"]["href"] == "http://pay"


@patch("app.lib.gov_uk_pay.requests.post")
def test_create_payment_failure(mock_post, test_app):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("fail")
    mock_post.return_value = mock_response

    with test_app.app_context():
        result = create_payment(1000, "desc", "ref", "test@email.com", "http://return")
        assert result is None


def test_validate_payment_success(test_app):
    with test_app.app_context():
        data = {"state": {"status": "success"}}
        assert validate_payment(data) is True


def test_validate_payment_failed(test_app):
    with test_app.app_context():
        data = {"state": {"status": "failed"}}
        assert validate_payment(data) is False


def test_validate_payment_status_none(test_app):
    with test_app.app_context():
        data = {"state": {"status": None}}
        assert validate_payment(data) is False
