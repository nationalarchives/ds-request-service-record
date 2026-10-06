# State machine

The user journey is controlled by a per-request routing state machine.

## What it does

The state machine decides which page comes next after each form submission. Route handlers do not hard-code the next
URL; instead, they ask the state machine which route should follow based on a combination of business rules, information
provided by the user and API responses.

## Where it lives

Relevant code:

- `app/lib/decorators/state_machine_decorator.py`
- `app/lib/state_machine/state_machine.py`
- `app/main/routes/routes.py`

## How it works

The `with_state_machine` decorator creates a new `RoutingStateMachine` for each request and stores it on Flask’s
request-scoped `g` object. That means any code running in the same request can access the current state machine without
passing it around manually.

A typical route flow looks like this:

1. the view receives the form and state machine
2. the form validates successfully
3. the route calls a `continue_from_*()` method on the state machine
4. the route redirects to `state_machine.route_for_current_state`

That pattern keeps the journey logic in one place and avoids scattering branching rules across templates and route
handlers.

For the form-submission pattern we use across the site, see [Post-Redirect-Get](post-redirect-get.md).

## Why this matters

This approach makes a complex service like Request a Military Service record much easier to maintain because:

- route transitions are centralised
- journey changes are easier to reason about and test

## Related tests

- state machine route behaviour is tested extensively, both in Pytest and Playwright
- navigation helper tests cover route changes that depend on journey state
