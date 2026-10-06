# Template approach

We intentionally avoid logic in templates and duplicate templates where users need subtly different
content. This is a deliberate design choice that makes the service easier to reason about and maintain.

## What this means

Templates should simply render the data they are given. As a rule, we keep branching and most presentation choices in
Python rather than spreading them through template logic.

That often means the codebase contains multiple templates that look similar. **That is deliberate**: it is usually
easier to
reason about a few explicit, slightly repetitive templates than a single highly abstracted one with lots of
conditionals.

## Why we do this

This approach makes the service easier to maintain because:

- the rendered output is more deterministic
- it is easier to see which page is responsible for which content
- behaviour changes stay in route or form code instead of being hidden in templates
- similar pages remain straightforward to test and compare

## Where it shows up

Relevant code:

- `app/templates/`
- `app/main/routes/routes.py`
- `app/lib/content.py`

## Related ideas

This approach works alongside the other core patterns documented in this site:

- structured content loaded from YAML
