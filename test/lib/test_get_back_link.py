import pytest
from unittest.mock import patch
from app.lib.get_back_link import get_back_link

@pytest.fixture
def mock_session(monkeypatch):
    session = {}
    monkeypatch.setattr("app.lib.get_back_link.session", session)
    return session

@patch("app.lib.get_back_link.MultiPageFormRoutes")
def test_returns_previous_page_from_history(mock_routes, mock_session):
    mock_session["journey_history"] = ["/page1", "/page2", "/page3"]
    result = get_back_link()
    assert result == "/page2"

@patch("app.lib.get_back_link.MultiPageFormRoutes")
def test_returns_fallback_when_history_empty(mock_routes, mock_session):
    mock_session["journey_history"] = []
    mock_routes.BEFORE_YOU_START.value = "/before-you-start"
    result = get_back_link()
    assert result == "/before-you-start"

@patch("app.lib.get_back_link.MultiPageFormRoutes")
def test_returns_fallback_when_history_has_one_entry(mock_routes, mock_session):
    mock_session["journey_history"] = ["/page1"]
    mock_routes.BEFORE_YOU_START.value = "/before-you-start"
    result = get_back_link()
    assert result == "/before-you-start"

@patch("app.lib.get_back_link.MultiPageFormRoutes")
def test_returns_fallback_when_history_missing(mock_routes, mock_session):
    # No "journey_history" key in session
    mock_routes.BEFORE_YOU_START.value = "/before-you-start"
    result = get_back_link()
    assert result == "/before-you-start"
