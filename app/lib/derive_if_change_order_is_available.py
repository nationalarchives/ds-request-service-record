"""
Module for deriving if a user can change their order type.

A user can change their order if:
1. The service person was NOT an officer, OR
2. The service person was an officer AND the service branch is RAF
"""

from typing import Optional


def derive_if_change_order_is_available(form_data: Optional[dict]) -> bool:
    """
    Determine if a user can change their order type based on form data.

    Args:
        form_data: Dictionary containing form submission data with keys:
                  - were_they_a_commissioned_officer: "yes", "no", or "unknown"
                  - service_branch: Service branch identifier (e.g., "ROYAL_AIR_FORCE")

    Returns:
        bool: True if the user can change their order, False otherwise.
              Returns True if:
              - Service person was not an officer (was "no"), OR
              - Service person may have been an officer (was "unknown"), OR
              - Service person was an officer ("yes") AND service branch is "ROYAL_AIR_FORCE"

              Returns False in all other cases.
    """
    if form_data is None:
        return False

    officer_status = form_data.get("were_they_a_commissioned_officer")
    service_branch = form_data.get("service_branch")

    # If service person was not an officer, return True
    if officer_status == "no":
        return True

    # If officer status is unknown, return True
    if officer_status == "unknown":
        return True

    # If service person was an officer AND service branch is RAF, return True
    if officer_status == "yes" and service_branch == "ROYAL_AIR_FORCE":
        return True

    # All other cases
    return False
