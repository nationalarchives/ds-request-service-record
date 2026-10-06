# Post-Redirect-Get

The service uses the Post-Redirect-Get pattern across the site for form submissions.

## What it does

When a form is submitted successfully, the server responds with a redirect instead of rendering the next page directly. The browser then follows that redirect with a GET request.

## Where it lives

Relevant code:

- `app/main/routes/routes.py`
- `app/lib/decorators/state_machine_decorator.py`
- `app/lib/state_machine/state_machine.py`

## How it works

A typical flow looks like this:

1. the browser submits a POST request
2. the server validates the form and updates journey state as needed
3. the server returns a redirect
4. the browser follows the redirect with a GET request

## Why this matters

This pattern helps us:

- avoid duplicate submissions if the user refreshes after posting
- keep the URL in sync with the current step in the journey
- ensure form handling is consistent across the service

## Related tests

- the main route tests exercise the redirect behaviour after successful form submissions
