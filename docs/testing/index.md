# Testing

The test suite covers the service’s core patterns as well as lower-level helper behaviour.

## Topics

- **Playwright** — end-to-end browser tests covering journeys, protected routes, and shared checks across pages
- **Unused content** — checks that YAML content entries are actually referenced by templates or forms
- **Navigation helpers** — checks the dynamic back-link helpers used by the journey

## Why these tests matter

These tests help us keep the content structure, request flow, navigation behaviour, and browser-level user experience aligned as the service changes.
