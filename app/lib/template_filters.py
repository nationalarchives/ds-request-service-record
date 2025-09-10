import re


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
        text, url = match.group(1), match.group(2)
        return f'<a href="{url}">{text}</a>'
    return pattern.sub(replacer, s)
