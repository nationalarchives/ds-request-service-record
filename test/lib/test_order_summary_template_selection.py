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

    def test_army_officer_full_record_check_digital_combination(self):
        """Should return army-officer-full-record-check-digital template for army officer processing + digital delivery"""
        order_data = {
            "service_branch": "BRITISH_ARMY",
            "were_they_a_commissioned_officer": "yes",
            "processing_option": "full",
            "delivery_type": "Digital",
        }
        result = get_order_summary_template_variant(order_data)
        assert (
            result
            == "your-order-summary-full-record-check-british-army-officer-digital"
        )

    def test_army_officer_full_record_check_printed_combination(self):
        """Should return army-officer-full-record-check-printed template for army officer processing + printed delivery"""
        order_data = {
            "service_branch": "BRITISH_ARMY",
            "were_they_a_commissioned_officer": "yes",
            "processing_option": "full",
            "delivery_type": "PrintedTracked",
        }
        result = get_order_summary_template_variant(order_data)
        assert (
            result
            == "your-order-summary-full-record-check-british-army-officer-printed"
        )

    def test_army_non_officer_full_record_check_printed_uses_default_template(self):
        """Should return the default full-record-check-printed template when British Army record is not for an officer"""
        order_data = {
            "service_branch": "BRITISH_ARMY",
            "were_they_a_commissioned_officer": "no",
            "processing_option": "full",
            "delivery_type": "PrintedTracked",
        }
        result = get_order_summary_template_variant(order_data)
        assert result == "your-order-summary-full-record-check-printed"

    def test_raf_officer_full_record_check_digital_uses_default_template(self):
        """Should return the default full-record-check-digital template when commissioned officer is not in the British Army"""
        order_data = {
            "service_branch": "ROYAL_AIR_FORCE",
            "were_they_a_commissioned_officer": "yes",
            "processing_option": "full",
            "delivery_type": "Digital",
        }
        result = get_order_summary_template_variant(order_data)
        assert result == "your-order-summary-full-record-check-digital"

    def test_standard_processing_ignores_army_officer_fields(self):
        """Should return the standard template when officer-specific fields are present with standard processing"""
        order_data = {
            "service_branch": "BRITISH_ARMY",
            "were_they_a_commissioned_officer": "yes",
            "processing_option": "standard",
            "delivery_type": "Digital",
        }
        result = get_order_summary_template_variant(order_data)
        assert result == "your-order-summary-standard-digital"

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
