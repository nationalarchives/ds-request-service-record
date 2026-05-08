"""
Unit tests for derive_if_change_order_is_available function.
"""

from app.lib.derive_if_change_order_is_available import (
    derive_if_change_order_is_available,
)


class TestDeriveIfChangeOrderIsAvailable:
    """Test suite for derive_if_change_order_is_available function."""

    # Tests for non-officer status
    def test_returns_true_when_service_person_is_not_an_officer(self):
        """Test that True is returned when service person is not an officer."""
        form_data = {
            "were_they_a_commissioned_officer": "no",
            "service_branch": "BRITISH_ARMY",
        }
        assert derive_if_change_order_is_available(form_data) is True

    def test_returns_true_for_non_officer_regardless_of_service_branch(self):
        """Test that True is returned for non-officer regardless of service branch."""
        service_branches = [
            "ROYAL_NAVY",
            "BRITISH_ARMY",
            "ROYAL_AIR_FORCE",
            "HOME_GUARD",
            "OTHER",
            "UNKNOWN",
        ]
        for branch in service_branches:
            form_data = {
                "were_they_a_commissioned_officer": "no",
                "service_branch": branch,
            }
            assert derive_if_change_order_is_available(form_data) is True

    # Tests for officer status with RAF
    def test_returns_true_when_officer_and_service_branch_is_raf(self):
        """Test that True is returned when service person is an officer in RAF."""
        form_data = {
            "were_they_a_commissioned_officer": "yes",
            "service_branch": "ROYAL_AIR_FORCE",
        }
        assert derive_if_change_order_is_available(form_data) is True

    # Tests for officer status without RAF
    def test_returns_false_when_officer_and_service_branch_is_not_raf(self):
        """Test that False is returned when service person is an officer but not in RAF."""
        service_branches = [
            "ROYAL_NAVY",
            "BRITISH_ARMY",
            "HOME_GUARD",
            "OTHER",
            "UNKNOWN",
        ]
        for branch in service_branches:
            form_data = {
                "were_they_a_commissioned_officer": "yes",
                "service_branch": branch,
            }
            assert derive_if_change_order_is_available(form_data) is False

    # Tests for unknown officer status
    def test_returns_false_when_officer_status_is_unknown(self):
        """Test that False is returned when officer status is unknown."""
        service_branches = [
            "ROYAL_NAVY",
            "BRITISH_ARMY",
            "ROYAL_AIR_FORCE",
            "HOME_GUARD",
            "OTHER",
            "UNKNOWN",
        ]
        for branch in service_branches:
            form_data = {
                "were_they_a_commissioned_officer": "unknown",
                "service_branch": branch,
            }
            assert derive_if_change_order_is_available(form_data) is True
