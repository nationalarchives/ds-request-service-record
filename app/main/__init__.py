from app.lib.requires_session_key import requires_session_key
from flask import Blueprint

bp = Blueprint("main", __name__)
bp.before_request(requires_session_key)

from app.main import routes  # noqa: E402,F401
from app.main.routes import dynamics_payment_routes  # noqa: E402,F401
from app.main.routes import request_payment_routes  # noqa: E402,F401
from app.main.routes import shared_payment_routes  # noqa: E402,F401
