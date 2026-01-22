import pytest

from app.lib.template_filters import format_standard_printed_order_price


def test_returns_none_when_s_is_none():
    assert format_standard_printed_order_price(None, 500, 250) is None


def test_replaces_single_delivery_fee_placeholder():
    s = "[DELIVERY_FEE]"
    assert (
        format_standard_printed_order_price(s, 500, 250)
        == "<span data-delivery-price>5.00</span>"
    )


def test_replaces_single_order_type_fee_placeholder():
    s = "[ORDER_TYPE_FEE]"
    assert (
        format_standard_printed_order_price(s, 500, 250)
        == "<span data-order-type-price>2.50</span>"
    )


def test_replaces_both_placeholders_in_string():
    s = "Delivery fee: [DELIVERY_FEE], Order type fee: [ORDER_TYPE_FEE]"
    assert (
        format_standard_printed_order_price(s, 1234, 567)
        == "Delivery fee: <span data-delivery-price>12.34</span>, Order type fee: <span data-order-type-price>5.67</span>"
    )


def test_replaces_multiple_occurrences_of_placeholders():
    s = "[DELIVERY_FEE] [DELIVERY_FEE] [ORDER_TYPE_FEE]"
    assert (
        format_standard_printed_order_price(s, 99, 1)
        == "<span data-delivery-price>0.99</span> <span data-delivery-price>0.99</span> <span data-order-type-price>0.01</span>"
    )


def test_leaves_string_unchanged_when_no_placeholders_present():
    s = "No placeholders to replace here"
    assert (
        format_standard_printed_order_price(s, 500, 250)
        == "No placeholders to replace here"
    )


def test_raises_type_error_when_fee_is_none_due_to_substitution():
    s = "Delivery fee: [DELIVERY_FEE] Order type fee: [ORDER_TYPE_FEE]"
    with pytest.raises(TypeError):
        format_standard_printed_order_price(s, None, 250)
    with pytest.raises(TypeError):
        format_standard_printed_order_price(s, 500, None)


def test_raises_type_error_when_s_is_not_str():
    with pytest.raises(TypeError):
        format_standard_printed_order_price(123, 500, 250)
