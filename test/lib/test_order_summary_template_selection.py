import pytest

from app.lib.order_summary_template_selection import get_order_summary_template_variant


class TestGetOrderSummaryTemplateVariant:
    """Tests for get_order_summary_template_variant function"""

    def test_standard_printed_combination(self):
        """Should return standard-printed template for standard processing + printed delivery"""
        order_data = {
            "processing_option": "standard",
            "delivery_type": "PrintedTracked",
        }
        result = get_order_summary_template_variant(order_data)
        assert result == "your-order-summary-standard-printed"

    def test_standard_digital_combination(self):
        """Should return standard-digital template for standard processing + digital delivery"""
        order_data = {
            "processing_option": "standard",
            "delivery_type": "Digital",
        }
        result = get_order_summary_template_variant(order_data)
        assert result == "your-order-summary-standard-digital"

    def test_full_printed_combination(self):
        """Should return full-record-check-printed template for full processing + printed delivery"""
        order_data = {
            "processing_option": "full",
            "delivery_type": "PrintedTracked",
        }
        result = get_order_summary_template_variant(order_data)
        assert result == "your-order-summary-full-record-check-printed"

    def test_full_digital_combination(self):
        """Should return full-record-check-digital template for full processing + digital delivery"""
        order_data = {
            "processing_option": "full",
            "delivery_type": "Digital",
        }
        result = get_order_summary_template_variant(order_data)
        assert result == "your-order-summary-full-record-check-digital"

    def test_invalid_processing_option(self):
        """Should raise ValueError for invalid processing_option"""
        order_data = {
            "processing_option": "invalid",
            "delivery_type": "PrintedTracked",
        }
        with pytest.raises(ValueError) as exc_info:
            get_order_summary_template_variant(order_data)
        assert "Invalid combination" in str(exc_info.value)

    def test_invalid_delivery_type(self):
        """Should raise ValueError for invalid delivery_type"""
        order_data = {
            "processing_option": "standard",
            "delivery_type": "InvalidDelivery",
        }
        with pytest.raises(ValueError) as exc_info:
            get_order_summary_template_variant(order_data)
        assert "Invalid combination" in str(exc_info.value)

    def test_missing_processing_option(self):
        """Should raise ValueError when processing_option is missing"""
        order_data = {
            "delivery_type": "PrintedTracked",
        }
        with pytest.raises(ValueError) as exc_info:
            get_order_summary_template_variant(order_data)
        assert "Invalid combination" in str(exc_info.value)

    def test_missing_delivery_type(self):
        """Should raise ValueError when delivery_type is missing"""
        order_data = {
            "processing_option": "standard",
        }
        with pytest.raises(ValueError) as exc_info:
            get_order_summary_template_variant(order_data)
        assert "Invalid combination" in str(exc_info.value)

    def test_none_processing_option(self):
        """Should raise ValueError when processing_option is None"""
        order_data = {
            "processing_option": None,
            "delivery_type": "PrintedTracked",
        }
        with pytest.raises(ValueError) as exc_info:
            get_order_summary_template_variant(order_data)
        assert "Invalid combination" in str(exc_info.value)

    def test_none_delivery_type(self):
        """Should raise ValueError when delivery_type is None"""
        order_data = {
            "processing_option": "standard",
            "delivery_type": None,
        }
        with pytest.raises(ValueError) as exc_info:
            get_order_summary_template_variant(order_data)
        assert "Invalid combination" in str(exc_info.value)
