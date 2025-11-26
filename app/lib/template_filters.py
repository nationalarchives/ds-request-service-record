import re
from app.constants import ExternalLinks


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

    def replacer(match):
        text = match.group(1)
        key = match.group(2).strip()
        url = getattr(ExternalLinks, key, key)
        return f'<a href="{url}" target="_blank" rel="noreferrer noopener">{text}</a>'

    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]+\")?\)")
    return link_pattern.sub(replacer, s)
