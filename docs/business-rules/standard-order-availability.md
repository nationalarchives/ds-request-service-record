# Standard order availability

Users who reach the order stage will be presented with either a "Choose your order type" page or a "Your order type"
page, depending on whether a **Standard** order is available for the record they are requesting.

The state machine in `app/lib/state_machine/state_machine.py` determines which order page users see.

## Changing an order from the "Your order summary" page

Only users who originally had a choice of order type see the **Change order** link on the **Your order
summary** page. The link returns them to "Choose your order type".

`app/lib/derive_if_change_order_is_available.py` applies the corresponding rule for the summary link.
