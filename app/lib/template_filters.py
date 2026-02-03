import re
from datetime import datetime
from urllib.parse import urlencode

from app.constants import ExternalLinks
from app.lib.boundary_years import BoundaryYears
from jinja2 import pass_context


def slugify(s):
    if not s:
        return s
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


def parse_markdown_links(s, new_tab=True):
    if not s:
        return s
    # Regex to match [text](url)
    pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    def replacer(match):
        text = match.group(1)
        key = match.group(2).strip()
        url = getattr(ExternalLinks, key, key)
        attrs = ' target="_blank" rel="noreferrer noopener"' if new_tab else ""
        return f'<a href="{url}"{attrs}>{text}</a>'

    return pattern.sub(replacer, s)


def inject_unique_survey_link(s, current_endpoint=None):
    if not s:
        return s

    match = re.search(r"\[([^\]]+)\]\(([^)]+)\)", s)
    if not match:
        return s

    link_text = match.group(1)
    # We use the key from the Markdown to look up the property in ExternalLinks
    key = match.group(2).strip()
    link_url = getattr(ExternalLinks, key, key)

    current_page = ""
    if current_endpoint:
        current_page = re.sub(r"[a-z]*\.", "", current_endpoint).strip()

    query_string = urlencode({"current_page": current_page}) if current_page else ""
    url = f"{link_url}?{query_string}" if query_string else link_url

    replacement = (
        f'<a href="{url}" target="_blank" rel="noreferrer noopener">{link_text}</a>'
    )
    # Replace only the first match. This function is not a general-purpose link parser
    return re.sub(r"\[([^]]+)]\(([^)]+)\)", replacement, s, count=1)


def parse_bold_text(s):
    if not s:
        return s
    # Regex to match **text** (non-greedy)
    pattern = re.compile(r"\*\*(.+?)\*\*")

    def replacer(match):
        text = match.group(1)
        return f"<strong>{text}</strong>"

    return pattern.sub(replacer, s)


def parse_first_birth_year_for_closed_records(s):
    if not s:
        return s

    year = BoundaryYears.first_birth_year_for_closed_records(datetime.now().year)

    span = f"<span data-last-birth-year-for-open-records='{year}'>{year}</span>"

    return s.replace(
        "[FIRST_BIRTH_YEAR_FOR_CLOSED_RECORDS]",
        span,
    )


def format_standard_printed_order_price(s, delivery_fee, order_type_fee):
    if s is None:
        return s

    if delivery_fee is None:
        raise TypeError("delivery_fee cannot be None")
    if order_type_fee is None:
        raise TypeError("order_type_fee cannot be None")

    values = {
        "DELIVERY_FEE": f"<span data-delivery-price>{convert_pence_to_pounds_string(delivery_fee)}</span>",
        "ORDER_TYPE_FEE": f"<span data-order-type-price>{convert_pence_to_pounds_string(order_type_fee)}</span>",
    }

    pattern = re.compile(r"\[(DELIVERY_FEE|ORDER_TYPE_FEE)\]")

    def replacer(m):
        return values[m.group(1)]

    return pattern.sub(replacer, s)


def convert_pence_to_pounds_string(pence):
    if pence is None:
        return None
    pounds = float(pence) / 100
    return f"{pounds:.2f}"


@pass_context
def prepare_page_title(ctx, title):
    PAGE_HEADING_LENGTH_LIMIT = 25

    form = ctx.get("form")
    content = ctx.get("content")

    has_errors = bool(getattr(form, "errors", None))

    app_title = None
    if content is not None:
        try:
            app_title = content["app"]["title"]
        except Exception:
            app = getattr(content, "app", None)
            app_title = getattr(app, "title", None)

    prefix = "Error: " if has_errors else ""
    page_title = str(title or "")

    # If the page_title is longer than the limit, we want to omit
    # the app_title from the resulting string.
    # This is to avoid overly long titles in the `<title>` tag.
    if len(page_title) >= PAGE_HEADING_LENGTH_LIMIT:
        app_title = ""
    else:
        app_title = f"{app_title}" if app_title else ""

    app_title = f"{app_title}" if app_title else ""

    parts = [p.strip() for p in (page_title, app_title) if p]
    return prefix + " - ".join(parts)
