from flask import session

from app.constants import MultiPageFormRoutes


def get_dynamic_back_link_route(key: str):
    dynamic_back_links = session.get("dynamic_back_links", {})
    route = dynamic_back_links.get(key, MultiPageFormRoutes.JOURNEY_START.value)
    return route
