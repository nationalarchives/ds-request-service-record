# Back links

Some pages in the journey can be reached through more than one path, so the Back link needs to be set dynamically.

## What it does

The application stores back-link destinations in the session and uses them to decide where the Back link should point
for a given page.

## Where it lives

Relevant code:

- `app/lib/decorators/update_dynamic_back_link_mapping.py`
- `app/lib/get_dynamic_back_link_route.py`
- `app/main/routes/routes.py`

## How it works

The `update_dynamic_back_link_mapping()` decorator updates a `dynamic_back_links` session value with the route mappings
that should apply.

Later, `get_dynamic_back_link_route()` reads from that session data and returns the correct route for the current
endpoint. If no custom mapping exists, it falls back to the start of the journey.

## Why this matters

This pattern keeps the user experience consistent on pages that are shared by multiple paths through the service. It
avoids hard-coding a single "Back" link destination when the journey needs to remember how the user arrived there.

## Related tests

- `test/main/test_get_dynamic_back_link_route.py`
- `test/main/decorators/test_update_dynamic_back_link_mapping.py`
