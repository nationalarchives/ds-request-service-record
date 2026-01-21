import requests
from app.constants import FALLBACK_COUNTRY_CHOICES
from app.lib.cache import cache
from flask import current_app

CACHE_KEY = "country_choices"
CACHE_TIMEOUT = 43200  # 12 hours in seconds


def get_country_choices():
    """Fetch country choices from the Record Copying Service API with caching.

    Retrieves a list of countries from the external API and caches the result
    for 12 hours to reduce API calls. Always places "United Kingdom" first in
    the list for user convenience. Falls back to a static list if the API call
    fails.

    Returns:
        list[str]: Sorted list of country names with UK first

    Note:
        The result is cached in Redis to avoid repeated API calls.
        Cache is automatically refreshed after 12 hours or if the
        cache is cleared.
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
