import re
from datetime import UTC, datetime
from urllib.parse import urlencode

from flask import url_for
from jinja2 import pass_context
from tna_utilities.string import slugify as slugify_util

from app.constants import ExternalLinks, MultiPageFormRoutes
from app.lib.boundary_years import BoundaryYears

MARKDOWN_LINK_PATTERN = re.compile(r"\[([^]]+)]\(([^)]+)\)")


def slugify(s):
    return slugify_util(s)


def resolve_markdown_link_target(target):
    # Markdown links now have an explicit target type so content is self-describing.
    # We only support:
    # - external:EXTERNAL_LINK_NAME  -> looked up on ExternalLinks
    # - route:ROUTE_NAME             -> looked up on MultiPageFormRoutes and built with url_for
    # Anything else is rejected so raw URLs and typos fail loudly.
    target = target.strip()

    if target.startswith("external:"):
        external_key = target.removeprefix("external:").strip()
        if not external_key:
            raise ValueError(
                "External markdown links must use an ExternalLinks constant after 'external:'."
            )
        if not hasattr(ExternalLinks, external_key):
            raise ValueError(
                f"Unknown external markdown link target '{external_key}'. Markdown links must use an ExternalLinks constant after 'external:'."
            )
        return getattr(ExternalLinks, external_key), False

    if target.startswith("route:"):
        route_name = target.removeprefix("route:").strip()
        if not route_name:
            raise ValueError(
                "Route markdown links must use a MultiPageFormRoutes member name after 'route:'."
            )
        if not hasattr(MultiPageFormRoutes, route_name):
            raise ValueError(
                f"Unknown route markdown link target '{route_name}'. Markdown links must use a MultiPageFormRoutes member name after 'route:'."
            )
        endpoint = getattr(MultiPageFormRoutes, route_name).value
        return url_for(endpoint), True

    raise ValueError(
        f"Unknown markdown link target '{target}'. Markdown links must use external:EXTERNAL_LINK_NAME or route:ROUTE_NAME."
    )


def parse_markdown_links(s, new_tab=True):
    if not s:
        return s

    def replacer(match):
        text = match.group(1)
        target = match.group(2).strip()
        url, is_internal_route = resolve_markdown_link_target(target)

        # external: links behave like our existing outbound links and can still opt
        # into opening in a new tab. route: links are internal navigation, so they
        # stay in the same tab even when new_tab=True.
        attrs = ""
        if not is_internal_route and new_tab:
            attrs = ' target="_blank" rel="noreferrer noopener"'
        return f'<a href="{url}"{attrs}>{text}</a>'

    return MARKDOWN_LINK_PATTERN.sub(replacer, s)


def inject_unique_survey_link(s, current_endpoint=None):
    if not s:
        return s

    match = MARKDOWN_LINK_PATTERN.search(s)
    if not match:
        return s

    link_text = match.group(1)
    target = match.group(2).strip()

    # Survey links always point to an external service, so we reject route:
    # targets before trying to resolve them through Flask routing.
    if target.startswith("route:"):
        raise ValueError(
            "Survey markdown links must use external:EXTERNAL_LINK_NAME targets."
        )

    link_url, _ = resolve_markdown_link_target(target)

    current_page = ""
    if current_endpoint:
        current_page = re.sub(r"[a-z]*\.", "", current_endpoint).strip()

    query_string = urlencode({"current_page": current_page}) if current_page else ""
    url = f"{link_url}?{query_string}" if query_string else link_url

    replacement = (
        f'<a href="{url}" target="_blank" rel="noreferrer noopener">{link_text}</a>'
    )
    # Replace only the first match. This function is not a general-purpose link parser
    return MARKDOWN_LINK_PATTERN.sub(replacement, s, count=1)


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

    year = BoundaryYears.first_birth_year_for_closed_records(datetime.now(UTC).year)

    span = f"<span data-first-birth-year-for-closed-records='{year}'>{year}</span>"

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

    pattern = re.compile(r"\[(DELIVERY_FEE|ORDER_TYPE_FEE)]")

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
        except (KeyError, TypeError):
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


def prepare_page_type_for_analytics_meta_tag(request_path):
    if not request_path:
        return ""

    # Coerce string and remove whitespace
    value = str(request_path).strip()
    if not value:
        return ""

    # Remove leading and trailing slashes
    value = value.strip("/")

    base = "request-a-military-service-record"
    suffix = "ramsr"

    # If we're at the base path, return the base path and suffix
    if value == base:
        return f"{base}_{suffix}"

    # If we're on another path, remove the base path, normalise to the first segment,
    # and append the suffix so page_type stays stable and does not include dynamic IDs.
    if value.startswith(f"{base}/"):
        rest = value.removeprefix(f"{base}/")
        first_segment = rest.split("/", 1)[0] if rest else ""
        if not first_segment:
            return f"{base}_{suffix}"
        return f"{first_segment}_{suffix}"

    return value
