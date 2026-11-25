# Feature flags

Feature flags let us merge changes without releasing them immediately. Flags are
environment variables, disabled by default, rather than user-facing settings.

## Configuration

Define flags in the `Features` class in `config.py`. For example:

```python
class Features:
    ENABLE_FEATURE_13: bool = strtobool(os.getenv("ENABLE_FEATURE_13", "False"))
```

`Production` inherits from `Features`; `Staging`, `Develop` and `Test` inherit
from `Production`. Flags default to `False` when the variable is absent, except
that `ENABLE_FEATURE_13` defaults to `True` in Staging. An explicit environment
value overrides that default.

Use the existing `strtobool` helper to convert environment strings to booleans.
It accepts values such as `True` and `False`, case-insensitively, and raises
`ValueError` for unrecognised values. An invalid flag prevents configuration
from loading rather than silently selecting a behaviour.

Application code reads the parsed boolean through Flask configuration:

```python
current_app.config["ENABLE_FEATURE_13"]
```

For journey changes, keep the flag check in a named
[state-machine condition](state-machine.md), alongside the other routing rules.
Do not read environment strings directly in route handlers or treat the string
`"False"` as a boolean: a non-empty string is truthy in Python.

Flags are evaluated when `config.py` loads. They are not live runtime switches:
the application must restart with the new environment to pick up a change.
Deployments stay on the existing behaviour unless the flag is explicitly enabled
in that deployment's environment or the environment-specific config defaults it
on.

## Enabling a flag locally

Docker Compose already loads the ignored `.env` file into the app container.
Set the flag there:

```dotenv
ENABLE_FEATURE_13=True
```

Recreate the app container so it receives the updated environment:

```sh
docker compose up -d --no-deps --force-recreate --wait app
```

Editing `.env` alone, or restarting the existing container without recreating
it, does not update the container's environment. Keep `.env.example` disabled
by default; local opt-in belongs in `.env`, not in committed configuration.

## Feature 13

`ENABLE_FEATURE_13` changes the destination after the commissioned-officer form
only when the service person was a British Army Commissioned Officer:

| Flag value        | Next page                                               |
| ----------------- | ------------------------------------------------------- |
| `False` (default) | We are unlikely to hold this record yet (Army guidance) |
| `True`            | We may hold this record                                 |

Other service branches and officer-status answers keep their existing routes.
When enabled, the flag also hides the Army records-transfer and waiting
paragraphs on the British Army order-type page. It does not change eligibility,
order options or prices.

## Testing

Unit tests set `current_app.config["ENABLE_FEATURE_13"]` explicitly to exercise
both values, regardless of the developer's local environment.

Keep flag-enabled browser checks in a dedicated spec rather than adding
conditional expectations to existing specs. For Feature 13, this is
`test/playwright/state-transitions/feature-13.spec.ts`.

The app and the Playwright runner are separate processes. Both need the flag:

1. Enable it in `.env` and recreate the app as described above.
2. Run the dedicated spec with the flag passed to Playwright:

```sh
ENABLE_FEATURE_13=True CI=true npx playwright test test/playwright/state-transitions/feature-13.spec.ts --project=chromium
```

The spec skips unless the runner receives exactly `ENABLE_FEATURE_13=True`.
This runner setting only controls whether the tests run; it does not enable
the feature in Flask. If the tests run but the app still uses the old route,
check `.env` and recreate the app container.

To return to normal browser testing, set `ENABLE_FEATURE_13=False` in `.env`,
recreate the app, and run the usual suite without the runner flag.

In CI, `.github/actions/playwright-tests/action.yml` runs the existing suite
with the default-off app first. Subsequent steps enable the flag, recreate the
app, and run only the dedicated Feature 13 spec. The existing specs and shared
helpers do not need flag-dependent expectations (and we definitely don't want
to be unnecessarily running hundreds of tests twice for a single transition).
