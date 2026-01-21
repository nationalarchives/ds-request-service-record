from app.constants import MultiPageFormRoutes
from flask import session


def get_dynamic_back_link_route(key: str):
    """Retrieve the dynamic back link route for a given page key.

    Dynamic back links allow pages to have context-aware back buttons that
    remember where the user came from, rather than always going to the same page.

    Args:
        key (str): The route endpoint key to look up

    Returns:
        str: The route value to redirect to, defaults to journey start if not found
    """
    dynamic_back_links = session.get("dynamic_back_links", {})
    route = dynamic_back_links.get(key, MultiPageFormRoutes.JOURNEY_START.value)
    return route
