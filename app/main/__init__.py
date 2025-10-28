from flask import Blueprint

bp = Blueprint("main", __name__)

from app.main import routes  # noqa: E402,F401
from app.main.routes import payment_routes  # noqa: E402,F401
