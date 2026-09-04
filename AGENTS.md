# AGENTS.md

Guidance for AI coding agents and contributors working in this repository.

## Project summary

- Service: Flask app for requesting military service records.
- Runtime: Python 3.14 with Poetry.
- Primary execution environment: Docker Compose.
- Frontend assets: built with Sass and Webpack into `app/static`.
- App entrypoint: `main.py` (creates app via `app.create_app`).

## Repository map

- `app/`: Flask application package.
- `app/main/routes/`: user journey and payment routes.
- `app/main/forms/`: WTForms form definitions.
- `app/lib/`: shared helpers (content, state machine, db, API clients, etc.).
- `app/content/content.yaml`: CMS-like content for templates/pages.
- `templates/`: Jinja templates.
- `test/`: pytest and unittest-style tests.
- `test/playwright/`: browser end-to-end tests.
- `wiremock/`: local mock API mappings.

## Local development

1. Start services:
   - `docker compose up -d`
2. If first run, restore static assets from node modules:
   - `docker compose exec app cp -r /app/node_modules/@nationalarchives/frontend/nationalarchives/assets /app/app/static`
3. Create DB schema if needed:
   - `docker compose exec app poetry run python create_database.py`

Useful local endpoints:

- App: `http://localhost:65517`
- WireMock: `http://localhost:65498`
- Adminer: `http://localhost:65502`
- MkDocs: `http://localhost:65518`

## Build, lint, and test commands

Run commands inside the app container unless there is a clear reason not to.

- Python tests:
  - `docker compose exec app poetry run python -m pytest`
- Formatting/linting:
  - `docker compose exec app format`
- Frontend compile:
  - `docker compose exec app npm run compile`
- Frontend dev watch:
  - `docker compose exec app npm run dev`
- Playwright tests:
  - `docker compose exec app npm run test:playwright`

## Code patterns to preserve

- Keep route handlers in `app/main/routes/` thin and flow-oriented.
- Reuse existing decorators and helpers for state/session behavior:
  - `with_state_machine`
  - `with_form_prefilled_from_session`
  - `update_dynamic_back_link_mapping`
- Persist form/session values using existing save helpers instead of ad hoc session writes.
- For page content, prefer updates in `app/content/content.yaml` and existing template/filter conventions.

## Testing expectations for changes

- Route or form changes: update/add tests in `test/main/`.
- Utility/helper changes in `app/lib/`: update/add tests in `test/lib/`.
- Content-driven behavior changes: add assertions for rendered output and journey flow.
- UI or browser behavior changes: update/add Playwright coverage in `test/playwright/` where applicable.

## Database and payment flow cautions

- Avoid changing payment/state-machine transitions without corresponding tests.
- Keep database model updates backwards compatible unless migration strategy is explicit.
- Do not hardcode secrets, API keys, or environment-specific URLs.

## Agent editing guardrails

- Do not remove existing behavior unless requested.
- If adding a new dependency, justify it in the PR/change notes.
- Validate with the smallest relevant test set first, then broader tests if needed.

## Change workflow

1. Read related route/form/helper tests before editing.
2. Implement code changes.
3. Create necessary tests (Python and/or Playwright).
4. Run formatting/linting.
5. Run tests.
6. Summarize functional impact and any remaining risks.
