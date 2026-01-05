import pytest
import os


@pytest.fixture(scope="session")
def wiremock_url():
    """
    Get the WireMock server URL.
    
    Uses the Docker Compose service when running in CI/test environment,
    or can be overridden with WIREMOCK_URL environment variable.
    """
    return os.environ.get("WIREMOCK_URL", "http://localhost:65519/")


class WireMockServer:
    """Wrapper for WireMock server URL."""
    
    def __init__(self, base_url):
        self._base_url = base_url.rstrip('/')
    
    def url(self):
        """Get the base URL of the WireMock server."""
        return self._base_url + '/'


@pytest.fixture(scope="session")
def wiremock_server(wiremock_url):
    """
    Pytest fixture that provides access to the WireMock Docker server.
    
    Note: This expects the WireMock Docker container to be running.
    Start it with: docker-compose up mock-record-copying-service-api
    """
    return WireMockServer(wiremock_url)
