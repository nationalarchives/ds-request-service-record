from flask import current_app
from requests import JSONDecodeError, Timeout, TooManyRedirects, codes, get


class JSONAPIError(Exception):
    pass


class JSONAPIConnectionError(JSONAPIError):
    pass


class JSONAPITimeoutError(JSONAPIError):
    pass


class JSONAPIRedirectError(JSONAPIError):
    pass


class JSONAPIUnexpectedError(JSONAPIError):
    pass


class JSONAPINonJSONResponseError(JSONAPIError):
    pass


class JSONAPIBadRequestError(JSONAPIError):
    pass


class ResourceNotFound(Exception):
    pass


class ResourceForbidden(Exception):
    pass


class JSONAPIRequestFailedError(JSONAPIError):
    pass


class JSONAPIClient:
    def __init__(self, api_url, params=None, headers=None):
        self.api_url = api_url
        self.params = params.copy() if params else {}
        self.headers = headers.copy() if headers else {}

    def add_parameter(self, key, value):
        self.params[key] = value

    def add_parameters(self, params):
        self.params = self.params | params

    def get(self, path="/"):
        url = f"{self.api_url}/{path.lstrip('/')}"
        try:
            response = get(
                url,
                params=self.params,
                headers=self.headers,
            )
        except ConnectionError as e:
            current_app.logger.exception("JSON API connection error")
            raise JSONAPIConnectionError("A connection error occured") from e
        except Timeout as e:
            current_app.logger.exception("JSON API timeout")
            raise JSONAPITimeoutError("The request timed out") from e
        except TooManyRedirects as e:
            current_app.logger.exception("JSON API had too many redirects")
            raise JSONAPIRedirectError("Too many redirects") from e
        except Exception as e:
            current_app.logger.exception("Unknown JSON API exception")
            raise JSONAPIUnexpectedError(str(e)) from e
        current_app.logger.debug(response.url)
        if response.status_code == codes.ok:
            try:
                return response.json()
            except JSONDecodeError as e:
                current_app.logger.exception("JSON API provided non-JSON response")
                raise JSONAPINonJSONResponseError("Non-JSON response provided") from e
        if response.status_code == 400:
            current_app.logger.error(f"Bad request: {response.url}")
            raise JSONAPIBadRequestError("Bad request")
        if response.status_code == 403:
            current_app.logger.warning("Forbidden")
            raise ResourceForbidden("Forbidden")
        if response.status_code == 404:
            current_app.logger.warning("Resource not found")
            raise ResourceNotFound("Resource not found")
        current_app.logger.error(f"JSON API responded with {response.status_code}")
        raise JSONAPIRequestFailedError("Request failed")
