# Playwright

Playwright provides the end-to-end browser test coverage for this service.

## What it covers

The Playwright tests exercise the user journey in a real browser and help us verify that pages behave correctly when stitched together as a complete flow.

In this codebase, Playwright is used for:

- end-to-end journey tests
- direct-access and session-protection tests
- automated checks that apply across many pages, including HTML validation, accessibility checks, and analytics meta tags

## Where it lives

Relevant files:

- `playwright.config.ts`
- `package.json`
- `test/playwright/`
- `test/playwright/lib/step-functions.ts`
- `test/playwright/lib/constants.ts`

Representative specs:

- `test/playwright/end-to-end/to-order-summary-and-back.spec.ts`
- `test/playwright/prevent-direct-mid-journey-access.spec.ts`
- `test/playwright/tests-applicable-to-all-pages/tests-applicable-to-all-pages.spec.ts`

## How it is structured

### Configuration

`playwright.config.ts` defines:

- the Playwright test directory
- CI-specific timeout and worker behaviour
- retry behaviour
- trace collection on first retry
- browser and device coverage

The configured projects include:

- Chromium
- Firefox
- WebKit
- Mobile Chrome
- Mobile Safari

### Paths and reusable steps

`test/playwright/lib/constants.ts` defines named page paths so specs do not duplicate raw URLs.

`test/playwright/lib/step-functions.ts` contains reusable helpers for common actions such as:

- continuing from one step of the journey to the next
- checking validation messages
- asserting the current page and heading
- clicking Back links and verifying navigation

This keeps the tests readable and allows long journeys to be expressed as a sequence of named steps.

### Main test types

#### End-to-end journey tests

These tests follow the full service journey through multiple pages and verify that the expected page, content, price, or back-link behaviour is shown at each step.

`test/playwright/end-to-end/to-order-summary-and-back.spec.ts` is a representative example because it:

- progresses from the start of the service to the order summary
- checks order details
- then walks back up the journey to verify Back links

#### Direct-access and session tests

`test/playwright/prevent-direct-mid-journey-access.spec.ts` checks that protected pages cannot be opened directly without the expected session state, while exempt routes such as the index and healthcheck remain accessible.

These tests protect the assumptions made by the multi-step journey.

#### Tests applied to many pages

`test/playwright/tests-applicable-to-all-pages/tests-applicable-to-all-pages.spec.ts` iterates through the known page paths and runs shared checks against each one.

That includes:

- HTML validation
- automated accessibility checks
- analytics meta tag checks

## Why this matters

The Playwright suite gives us confidence that:

- the full user journey works across real browsers
- session and routing protections behave as expected
- navigation such as Back links works in context
- broad cross-cutting requirements can be checked consistently across many pages

## Running the tests

The npm scripts in `package.json` include:

- `test:playwright`
- `test:playwright:ui`

In this project, Playwright is usually run through the existing project tooling rather than as isolated test files.
