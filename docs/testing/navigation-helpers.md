# Navigation helpers

The navigation-helper tests cover the code that manages dynamic Back links.

## What they check

Relevant tests:

- `test/main/test_get_dynamic_back_link_route.py`
- `test/main/decorators/test_update_dynamic_back_link_mapping.py`

These tests verify that:

- a route is returned from the session when one is present
- the default journey start route is returned when there is no mapping
- the session mapping is updated correctly by the decorator
- existing mappings are preserved when new ones are added

## Why this matters

The Back link behaviour is route-dependent, so these tests help ensure that changes to the journey do not break the user’s path through the service.
