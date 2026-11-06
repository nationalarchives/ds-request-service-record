# Price calculations

There are two payments a user may have to make:

1. All users make an **initial payment**.
2. Users requesting a Full record check also make a **second payment**.

## Initial payment (Standard and Full record check)

The current base fees are defined in `OrderFeesPence` in `app/constants.py`:

| Order type        | Delivery format       | Base fee | Upfront total          |
| ----------------- | --------------------- | -------- | ---------------------- |
| Standard          | Digital               | £42.25   | Base fee               |
| Standard          | Printed, tracked post | £47.16   | Base fee plus delivery |
| Full record check | Digital               | £48.87   | Base fee               |
| Full record check | Printed, tracked post | £48.87   | Base fee               |

An explicitly stored delivery type is used to calculate the fee when present. Otherwise, delivery defaults to printed,
tracked post for [users without an email address](users-without-email.md), and digital for other users.

For **Standard printed** orders, the service obtains a delivery price from the Record Copying service
`GetDeliveryPrice` endpoint, using the destination country, tracked delivery and a fixed quantity of
10 colour pages at size A3. The returned price in pounds is converted to pence then added to the base fee.
A destination country is required.

## Second payment (Full record check only)

The upfront Full record check fee covers the search and page check only. The second payment covers copying and,
for printed delivery, postage and packaging.

The current per-page rates shown on the order summary are:

| Record category                   | Digital | Printed |
| --------------------------------- | ------- | ------- |
| British Army commissioned officer | £1.52   | £7.40   |
| Other records                     | £1.04   | £1.89   |

The rates shown to users are **explanatory content**, not derived from interaction with the Record Copying service.
journey.

The second-payment API accepts a quoted `net_amount` and an optional `delivery_amount`, with
the total calculated as:

```text
second payment total = net amount + delivery amount
```

If no delivery amount is supplied, it is zero.

## Where the rule lives

- `app/constants.py` defines the upfront base fees.
- `app/lib/price_calculations.py` selects fees and calculates Standard printed delivery.
- `app/lib/order_summary_data.py` prepares the summary's base fee and delivery breakdown.
- `app/main/routes/request_payment_routes.py` calculates the upfront amount for GOV.UK Pay.
- `app/main/routes/dynamics_payment_routes.py` accepts quoted second-payment amounts.
- `app/content/content.yaml` contains the displayed per-page rates and fee explanations.
