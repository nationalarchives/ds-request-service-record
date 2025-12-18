from app.sitemap import bp
from flask import make_response, render_template


@bp.route("/sitemap.xml")
def index():
    xml_sitemap_index = render_template(
        "sitemap.xml",
    )
    response = make_response(xml_sitemap_index)
    response.headers["Content-Type"] = "application/xml; charset=utf-8"
    return response
