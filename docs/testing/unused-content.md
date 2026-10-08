# Unused content

The unused-content test checks that entries in `app/content/content.yaml` are actually being used.

## What it checks

The test in `test/content/test_for_unused_content.py` does two things:

1. it scans the loaded YAML structure and checks that non-form keys appear in templates
2. it checks that form field content keys are referenced through `get_field_content(...)` in the form code

## Why it exists

This test helps us avoid dead content entries that no longer appear in the UI. That makes it easier for content designers and developers to understand which parts of the YAML file are still live.

## Related files

- `app/content/content.yaml`
- `app/lib/content.py`
- `test/content/test_for_unused_content.py`
- `test/content/test_get_field_content.py`
