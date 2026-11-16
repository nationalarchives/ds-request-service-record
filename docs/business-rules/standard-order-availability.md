# Standard order availability

Users who reach the order stage will be presented with either a "Choose your order type" page or a "Your order type"
page, depending on whether a **Standard** order is available for the record they are requesting.

The state machine in `app/lib/state_machine/state_machine.py` determines which order page users see.

## RAF non-commissioned officer records

Users requesting an RAF non-commissioned officer record can still choose either **Standard** or **Full record check**.
However, the page recommends **Standard**: these records are often short, and most of the information is available
through Standard. A **Full record check** remains an option, but it may provide no additional information.

The page also presents this as its prominent warning. Any applicable proof-of-death notice is shown as a regular
paragraph instead of a second warning, so it does not compete. The proof-of-death requirements themselves are unchanged.

## Changing an order from the "Your order summary" page

Only users who originally had a choice of order type see the **Change order** link on the **Your order
summary** page. The link returns them to "Choose your order type".

`app/lib/derive_if_change_order_is_available.py` applies the corresponding rule for the summary link.
