from flask import Blueprint

bp = Blueprint("main", __name__)

from app.main.routes import routes_single_form_journey, routes_multiple_forms_journey, routes_shared_by_both_approaches
