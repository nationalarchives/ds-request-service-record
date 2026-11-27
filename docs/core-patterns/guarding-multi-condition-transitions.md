# Guarding multi-condition transitions

Some state machine transitions depend on multiple conditions. They use the answer to an earlier question alongside the
current answer to decide which step the user should see next. For example, the transition from "Were they a commissioned
officer?" uses both the selected service branch and whether the person was a commissioned officer.

We have seen requests, likely from automated clients, reach the "Were they a commissioned officer?" page without
progressing through the preceding journey steps. Submitting the form without a service branch can leave no matching
state machine transition, causing an error to be reported to our monitoring platform. The guard below redirects these
users to branch selection instead.

## Guarding the "Were they a commissioned officer?" transition

The "Were they a commissioned officer?" form includes a hidden `service_branch` field normally populated from the
session when the page is loaded. On POST, the submitted value is used for routing and saved to the session; it is not
checked against the existing session value.

After the form validates, `were_they_a_commissioned_officer` in `app/main/routes/routes.py` checks that the submitted
branch is a name in `ServiceBranches`. If the field is missing, empty or unrecognised, the route logs a warning and
redirects to service branch selection without saving the submitted form or calling the state machine. The warning does
not include submitted values. Form validation errors take precedence over this check, and the journey-entry guard still
redirects requests without an established journey session to the start page.

The check accepts every recognised branch. Royal Navy and Home Guard normally bypass the officer page, and a
commissioned-officer answer of "yes" for either branch has no matching officer transition. This check does not handle
that case.

## Related tests

`test/main/test_were_they_a_commissioned_officer.py` covers invalid-branch redirects, logging and session preservation.
See also [State machine](state-machine.md) for normal journey routing.
