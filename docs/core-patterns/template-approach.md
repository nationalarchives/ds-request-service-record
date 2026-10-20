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

## Exceptions to the rule

This is a strict pattern, but not a dogma. There are rare exceptions where a very small amount of view layer logic will be the clearest option. For example, the `conditionallyAvailableLink` Jinja macro in
[app/templates/macros/conditionally-available-link.html](file:///Users/gjones/PycharmProjects/request-a-military-service-record/app/templates/macros/conditionally-available-link.html)
renders a link only when a flag says it should appear.

**These are exceptions where there is a clear need**. We should only introduce them when they genuinely simplify the code and when the alternative would be more confusing. In practice, that usually means:

- the logic is a narrow, presentation-only concern impacting a small piece of content
- the condition is simple enough to be expressed as a reusable macro

Any exception should always be implemented as a Jinja2 macro. **The user journey diagram must also be updated to reflect this.** If a condition starts to grow beyond a simple, readable helper, it should usually move back into the state machine.

In other words: template logic is still the exception, not the default.

## Where it shows up

Relevant code:

- `app/templates/`
- `app/main/routes/routes.py`
- `app/lib/content.py`

## Related ideas

This approach works alongside the other core patterns documented in this site:

- structured content loaded from YAML
