from flask import session
from app.constants import MultiPageFormRoutes


def get_back_link():
    history = session.get("journey_history", [])
    if len(history) > 1:
        return history[-2]  # Previous page
    return MultiPageFormRoutes.BEFORE_YOU_START.value  # Fallback
