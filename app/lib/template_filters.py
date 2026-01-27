import re
from datetime import datetime

from app.constants import ExternalLinks
from app.lib.boundary_years import BoundaryYears


def slugify(s):
    if not s:
        return s
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


def parse_markdown_links(s):
    if not s:
        return s
    # Regex to match [text](url)
    pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    def replacer(match):
        text = match.group(1)
        key = match.group(2).strip()
        url = getattr(ExternalLinks, key, key)
        return f'<a href="{url}" target="_blank" rel="noreferrer noopener">{text}</a>'

    return pattern.sub(replacer, s)


def parse_bold_text(s):
    if not s:
        return s
    # Regex to match **text** (non-greedy)
    pattern = re.compile(r"\*\*(.+?)\*\*")

    def replacer(match):
        text = match.group(1)
        return f"<strong>{text}</strong>"

    return pattern.sub(replacer, s)


def parse_last_birth_year_for_open_records(s):
    if not s:
        return s

    year = BoundaryYears.last_birth_year_for_open_records(datetime.now().year)

    span = f"<span data-last-birth-year-for-open-records='{year}'>{year}</span>"

    return s.replace(
        "[LATEST_BIRTH_YEAR_FOR_OPEN_RECORDS]",
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
