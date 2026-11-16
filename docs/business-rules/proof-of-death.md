# Proof of death

## Why we ask for proof of death for closed record requests

To protect personal data that might relate to a living person, we ask users to provide proof of death for [closed records](closed-records.md).

## When a proof of death is not required for a closed record

Standard orders for closed records do not require proof of death when the service person's birth **year** falls within this range:

```text
IF birth year is on or after (current year - 115)
AND birth year is before (current year - 100)
THEN proof of death is not required for a Standard order
```

Proof of death is required for Standard orders when the birth year is **in or after** `current year - 100`. For Full record checks, proof of death is required for all closed records.

!!! tip "These are calendar-year comparisons"
The day and month of birth are not part of the calculation. For example, in 2026, Standard orders for closed records with birth years from 1911 to 1925 inclusive do not require proof of death. Standard orders with birth years of 1926 or later require it.

## Notice on the "Choose your order type" page

When a service person's year of birth falls in the window after records close to the public but before Standard orders require proof of death, the "Choose your order type" page explains that a Full record check will require proof of death. How this notice is presented depends on the type of record:

| Request                              | How the proof-of-death notice is presented | Why                                                                                                                                    |
| ------------------------------------ | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| RAF non-commissioned officer records | As a regular paragraph                     | The page gives greater prominence to the warning that **a Full record check may provide no additional information** for these records. |
| All other requests                   | In a warning component                     | To give prominence to the warning that **the user's choice will affect the proof of death requirement**.                               |

This affects only how the notice is presented; it does not change when proof of death is required.

## Users can proceed without uploading proof of death

It is a requirement of Freedom of Information (FOI) legislation that users can submit a request without providing proof of death.

If proof of death is required and the user does not provide it, they can still continue. In this scenario an automated email is sent to the user explaining the requirement for a proof of death.

## Flowchart

```mermaid
flowchart TD
    closed{"Is the record closed?"}
    exempt{"Standard order AND birth year before current year - 100?"}
    notRequired["Proof of death not required"]
    required["Ask for proof of death"]
    uploaded{"Has the user provided proof of death?"}
    continue["User can continue"]
    contact["User can continue; automated email explains proof of death requirement"]

    closed -->|No| notRequired
    closed -->|Yes| exempt
    exempt -->|Yes| notRequired
    exempt -->|No| required
    notRequired --> continue
    required --> uploaded
    uploaded -->|Yes| continue
    uploaded -->|No| contact
```
