from flask import Blueprint

from app.lib.requires_session_key import requires_session_key

bp = Blueprint("main", __name__)
bp.before_request(requires_session_key)

from app.main import routes
from app.main.routes import (
    dynamics_payment_routes,
    request_payment_routes,
    shared_payment_routes,
)
