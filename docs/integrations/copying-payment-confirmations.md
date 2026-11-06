# Copying payment confirmations

Record copying payments are confirmed by sending JSON to the MOD Copying API.

## When a confirmation is sent

Once GOV.UK Pay confirms a successful copying payment, `process_valid_payment` in `app/lib/gov_uk_pay.py` marks it as `PAID`, saves the provider ID and UTC processing time, and calls `send_payment_to_mod_copying_app` in `app/lib/dynamics_handler.py`.

## API payload

The application sends an HTTP POST to `MOD_COPYING_API_URL` with `Content-Type: application/json` and the following payload:

| JSON field        | Value                                                                            |
| ----------------- | -------------------------------------------------------------------------------- |
| `CaseNumber`      | The payment's case number.                                                       |
| `PayReference`    | The payment's reference.                                                         |
| `GovUkProviderId` | The GOV.UK Pay provider ID.                                                      |
| `Amount`          | The total amount, including any delivery charge, converted from pence to pounds. |
| `Date`            | The UTC processing time formatted as `YYYY-MM-DD HH:MM:SS`.                      |

If the HTTP response passes `raise_for_status`, the payment is marked as `SENT`. A reported HTTP error is logged and leaves it as `PAID`. This payload does not resend the service person's details or the original request email.

## Retrying unsuccessful sends

`retry_paid_dynamics_payments.py` is intended to be run as a cron job. It resends API confirmations for copying payments still marked as `PAID`, in creation order, and marks successfully sent entries as `SENT`.

The API call and database update are separate operations. If a send succeeds but saving `SENT` fails, a later retry can send the same data again.

## Configuration

| Setting               | Purpose                                     |
| --------------------- | ------------------------------------------- |
| `MOD_COPYING_API_URL` | Endpoint for copying-payment confirmations. |
