# Closed records

The application classifies a record as closed or open using the service person's birth **year**.

The first birth year for closed records is calculated as:

```text
first closed birth year = current year - 115
```

Records for people born **before** this year are classified as open. Records for people born **in or after**
this year are classified as closed.

This is a calendar-year comparison, not an exact-age calculation: the day and month of birth do not affect
the classification. For example, in 2026 the cutoff is 1 January 1911. A person born on 31 December 1910
falls into the open category; a person born on 1 January 1911 falls into the closed category.
The cutoff advances each year.
