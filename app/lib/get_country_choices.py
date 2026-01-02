from functools import lru_cache

import requests
from app.constants import FALLBACK_COUNTRY_CHOICES
from flask import current_app


@lru_cache(maxsize=1)
def get_country_choices():
    """
    Fetches country choices from the Record Copying Service API.
    Caches the result to avoid repeated API calls.
    Returns a list of country names sorted alphabetically.
    If the API call fails, returns the default list stored in constants.py.
    """
    try:
        response = requests.get(current_app.config.get("COUNTRY_API_URL"), timeout=5)
        response.raise_for_status()
        countries_data = response.json()

        if countries_data:
            country_names = [country["Description"] for country in countries_data]
            return sorted(country_names)
    except Exception:
        current_app.logger.error(
            "Failed to fetch country choices from the API. Using default."
        )

    return FALLBACK_COUNTRY_CHOICES
