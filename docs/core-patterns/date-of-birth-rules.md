# Date of birth rules

Business rules arising from the service person's date of birth are an important part of the service. Two main
classes support this:

1. `DateOfBirth` retrieves a date string from the session and converts it to a Python `date`
2. `DateOfBirthRules` provides business logic related to date of birth.
3. `BoundaryYears` is a single-source of truth for the underlying year thresholds for the service.

## Why this exists

The service stores DOB values in session data as plain text such as `01 January 1926`. That is convenient for display and form round-tripping, but it is not useful for comparisons. Year-based rules need a real `date` object so we can ask questions like:

- do we need a proof of death for this service person?
- is the service person's date of birth within the acceptable range for this service?
- do we need to warn the user that a specific journey path will result in a requirement for proof of death?

## Where the code lives

Relevant code:

- `app/lib/date_of_birth.py`
- `app/lib/date_of_birth_rules.py`
- `app/lib/boundary_years.py`

## Parsing the DOB from session data

`app/lib/date_of_birth.py` is the adapter between human-readable session values and the rest of the application.

It exposes two helpers:

- `parse_date_of_birth()` converts strings like `01 January 1926` into a Python `date`
- `get_date_of_birth_from_session()` reads the value from `session['form_data']` and returns a normalised DOB when present

This keeps the session format isolated in one place. Callers do not need to know how the value is stored or whether it is malformed; they can just rely on a proper `date` or `None`.

## Applying business rules

`app/lib/date_of_birth_rules.py` contains pure rule methods. These do not depend on Flask request state or route handlers. Instead, they answer a single question based on the DOB and the current year.

Examples include:

- `is_born_too_late()` — whether the date of birth is too late
- `requires_proof_of_death_for_standard_order()` — whether a Standard request needs a proof of death
- `requires_proof_of_death_for_full_record_check()` — whether a Full record check request needs a proof of death
- `show_proof_of_death_warning()` — whether to show a warning about proof of death requirements at the point a user might select Full record check

All read from `BoundaryYears` for the underlying year thresholds for the service.

## Why this matters

A lot depends on the service person's date of birth. By separating concerns (parsing the stored date of birth, storing thresholds and making decisions), the service stays easier to reason about:

- the session and the user interface can keep their friendly human-readable format
- the business rules can operate on consistent `date` values
- tests can target the actual decision logic without depending on Flask session state

This keeps the DOB logic readable and reduces the chance of subtle mistakes when record-closure years change over time.
