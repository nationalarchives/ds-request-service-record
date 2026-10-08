# Content approach

The service content is stored outside the templates in `app/content/content.yaml`.

## What it does

The app loads structured content at runtime and passes it into templates and forms.

## Where it lives

Relevant code:

- `app/lib/content.py`
- `app/content/content.yaml`
- `app/main/routes/routes.py`
- `app/main/forms/`
- `app/templates/`

## How it works

The `load_content()` helper reads `app/content/content.yaml` with `yaml.safe_load()` and returns the parsed structure.
Route handlers call `load_content()` and pass the resulting object into the template context as `content`.

Forms then use the structured content for labels and messages, which keeps the form definitions consistent with the
shared YAML source.

## Why this matters

This approach helps us:

- keep all the content in one place, in a format that is easy to read and edit
- review content separately from behaviour
- detect unused content entries with tests

## Related tests

- `test/content/test_get_field_content.py`
- `test/content/test_for_unused_content.py`

The unused-content test is especially important because it checks that the YAML keys are actually referenced by
templates or forms. That helps prevent orphaned content from building up over time.
