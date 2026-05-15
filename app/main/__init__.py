from flask import Blueprint

from app.lib.requires_session_key import requires_session_key

bp = Blueprint("main", __name__)
bp.before_request(requires_session_key)

from app.main import routes  # noqa: E402,F401
from app.main.routes import (
    dynamics_payment_routes,  # noqa: E402,F401
    request_payment_routes,  # noqa: E402,F401
    shared_payment_routes,  # noqa: E402,F401
)
