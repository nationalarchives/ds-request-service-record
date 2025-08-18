import pytest
from app import create_app
from app.lib.gov_uk_pay import create_payment, is_webhook_signature_valid, process_webhook_data
from unittest.mock import patch, MagicMock
from app.lib.gov_uk_pay import GOV_UK_PAY_EVENT_TYPES

@pytest.fixture(scope="module")
def test_app():
    app = create_app("config.Test")
    with app.app_context():
        yield app

@patch("app.lib.gov_uk_pay.requests.post")
def test_create_payment_success(mock_post, test_app):
    mock_response = MagicMock()
    mock_response.json.return_value = {"payment_id": "abc123", "_links": {"next_url": {"href": "http://pay"}}}
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

def test_is_webhook_signature_valid(test_app):
    class DummyRequest:
        def __init__(self, data, signature):
            self._data = data
            self.headers = {"Pay-Signature": signature}
        def get_data(self):
            return self._data

    with test_app.app_context():
        test_app.config["GOV_UK_PAY_SIGNING_SECRET"] = "secret"
        import hmac, hashlib
        payload = b"test"
        signature = hmac.new(b"secret", payload, hashlib.sha256).hexdigest()
        req = DummyRequest(payload, signature)
        assert is_webhook_signature_valid(req) is True
        req = DummyRequest(payload, "wrong")
        assert is_webhook_signature_valid(req) is False


def test_process_webhook_events(test_app):
    with test_app.app_context():
        for event_type in GOV_UK_PAY_EVENT_TYPES:
            data = {"resource_id": "abc123", "event_type": event_type.value}
            record = MagicMock()
            record.forenames = "John"
            record.requester_email = "john.doe@email.com"
            record.payment_id = "abc123"
            with patch("app.lib.gov_uk_pay.get_service_record_request", return_value=record):
                with patch("app.lib.models.db.session.delete") as mock_delete, \
                     patch("app.lib.models.db.session.commit") as mock_commit:
                    process_webhook_data(data)
                    mock_delete.assert_called_with(record)
                    mock_commit.assert_called()

