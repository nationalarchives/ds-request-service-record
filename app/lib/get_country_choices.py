import requests
from app.constants import FALLBACK_COUNTRY_CHOICES
from app.lib.cache import cache
from flask import current_app

CACHE_KEY = "country_choices"
CACHE_TIMEOUT = 43200  # 12 hours


def get_country_choices():
    """
    Fetches country choices from the Record Copying Service API.
    Caches the result in Redis to avoid repeated API calls.
    Returns a list of country names sorted alphabetically.
    If the API call fails, returns the default list stored in constants.py.
    """
    cached_countries = cache.get(CACHE_KEY)
    if cached_countries is not None:
        return cached_countries

    try:
        response = requests.get(current_app.config.get("COUNTRY_API_URL"), timeout=5)
        response.raise_for_status()
        countries_data = response.json()

        if countries_data:
            country_names = [country["Description"] for country in countries_data]
            sorted_countries = sorted(country_names)

            if "United Kingdom" in sorted_countries:
                sorted_countries.remove("United Kingdom")
                sorted_countries.insert(0, "United Kingdom")

            cache.set(CACHE_KEY, sorted_countries, timeout=CACHE_TIMEOUT)
            return sorted_countries
    except Exception:
        current_app.logger.error(
            "Failed to fetch country choices from the API. Using default."
        )

    return FALLBACK_COUNTRY_CHOICES
