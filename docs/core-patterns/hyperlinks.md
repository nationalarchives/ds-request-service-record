# Hyperlinks

The service manages outbound hyperlinks through named constants rather than hard-coding URLs directly into templates or
content.

## What it does

Content can use markdown-style links such as `[Search Ancestry](ANCESTRY_SEARCH)`. When the page is rendered, the link
key is resolved against `ExternalLinks` and converted into an HTML anchor tag with relevant attributes (such as
`target="_blank"` and `rel="noreferrer noopener"`).

This lets us keep:

- link destinations in one place, without duplication
- content copy readable in `app/content/content.yaml`
- templates free from repeated hard-coded URLs

## Where it lives

Relevant code:

- `app/constants.py`
- `app/lib/template_filters.py`
- `app/__init__.py`
- `app/content/content.yaml`

Relevant tests:

- `test/lib/test_template_filter_markdown_links.py`

## How it works

### Link destinations

External URLs are defined in the `ExternalLinks` class in `app/constants.py`.

Examples include:

- `ANCESTRY_SEARCH`
- `FOI_REQUEST_GUIDANCE`
- `CONTACT_US`

### Markdown parsing

The `parse_markdown_links()` helper in `app/lib/template_filters.py` looks for markdown-style links in the form
`[text](target)`.

For each match, it:

1. extracts the link text
2. extracts the target value
3. checks whether the target matches a constant on `ExternalLinks`
4. falls back to the raw target value if there is no matching constant
5. returns an HTML `<a>` tag

By default, links are rendered with:

- `target="_blank"`
- `rel="noreferrer noopener"`

That behaviour can be turned off by calling the helper with `new_tab=False`.

## Special case: survey links

`inject_unique_survey_link()` in `app/lib/template_filters.py` handles a more specific case for survey links. It reads a
markdown link, resolves it through `ExternalLinks`, and appends the current page to the query string so the survey can
identify where the user came from.

## Why this matters

This approach makes links easier to maintain because:

- URLs can be updated (and seen) in one place
- content can reference named links instead of repeating long URLs
- templates stay simpler and more deterministic
- link rendering behaviour is consistent across the service
