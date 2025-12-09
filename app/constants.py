from enum import Enum
from functools import lru_cache

import requests
from flask import current_app


class MultiPageFormRoutes(Enum):
    HOW_WE_PROCESS_REQUESTS = "main.how_we_process_requests"
    BEFORE_YOU_START = "main.before_you_start"
    YOU_MAY_WANT_TO_CHECK_ANCESTRY = "main.you_may_want_to_check_ancestry"
    ARE_YOU_SURE_YOU_WANT_TO_CANCEL = "main.are_you_sure_you_want_to_cancel"
    YOU_HAVE_CANCELLED_YOUR_REQUEST = "main.you_have_cancelled_your_request"
    HAVE_YOU_CHECKED_THE_CATALOGUE = "main.have_you_checked_the_catalogue"
    SEARCH_THE_CATALOGUE = "main.search_the_catalogue"
    IS_SERVICE_PERSON_ALIVE = "main.is_service_person_alive"
    MUST_SUBMIT_SUBJECT_ACCESS_REQUEST = "main.must_submit_subject_access_request"
    ARE_YOU_SURE_YOU_WANT_TO_PROCEED_WITHOUT_PROOF_OF_DEATH = (
        "main.are_you_sure_you_want_to_proceed_without_proof_of_death"
    )
    SERVICE_BRANCH_FORM = "main.service_branch_form"
    ONLY_LIVING_SUBJECTS_CAN_REQUEST_THEIR_RECORD = (
        "main.only_living_subjects_can_request_their_record"
    )
    WERE_THEY_A_COMMISSIONED_OFFICER_FORM = "main.were_they_a_commissioned_officer"
    WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS = (
        "main.we_do_not_have_royal_navy_service_records"
    )
    WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY = (
        "main.we_are_unlikely_to_hold_officer_records__army"
    )
    WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF = (
        "main.we_are_unlikely_to_hold_officer_records__raf"
    )
    WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__GENERIC = (
        "main.we_are_unlikely_to_hold_officer_records__generic"
    )
    WE_ARE_UNLIKELY_TO_LOCATE_THIS_RECORD = "main.we_are_unlikely_to_locate_this_record"
    WE_MAY_HOLD_THIS_RECORD = "main.we_may_hold_this_record"
    WHAT_WAS_THEIR_DATE_OF_BIRTH = "main.what_was_their_date_of_birth"
    WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_AFTER = (
        "main.we_do_not_have_records_for_people_born_after"
    )
    SERVICE_PERSON_DETAILS = "main.service_person_details"
    DO_YOU_HAVE_A_PROOF_OF_DEATH = "main.do_you_have_a_proof_of_death"
    UPLOAD_A_PROOF_OF_DEATH = "main.upload_a_proof_of_death"
    HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST = "main.have_you_previously_made_a_request"
    YOUR_DETAILS = "main.your_details"
    YOUR_POSTAL_ADDRESS = "main.your_postal_address"
    CHOOSE_YOUR_ORDER_TYPE = "main.choose_your_order_type"
    SEND_TO_GOV_UK_PAY = "main.send_to_gov_uk_pay"
    REQUEST_SUBMITTED = "main.request_submitted"


class ServiceBranches(Enum):
    ROYAL_NAVY = "Royal Navy (including Royal Marines)"
    BRITISH_ARMY = "British Army"
    ROYAL_AIR_FORCE = "Royal Air Force"
    HOME_GUARD = "Home Guard"
    OTHER = "Other"
    UNKNOWN = "I do not know"


class OrderFeesPence(Enum):
    STANDARD_DIGITAL = 4225
    STANDARD_PRINTED = 4716
    FULL_DIGITAL = 4887
    FULL_PRINTED = 4887


class Ranks(Enum):
    OFFICER = "Officer"
    NON_OFFICER = "Non-Officer"


class ExternalLinks:
    SUBJECT_ACCESS_REQUEST_FORM = (
        "https://discovery.nationalarchives.gov.uk/mod-dsa-request-step1"
    )
    MOD_SERVICE = "https://www.gov.uk/get-copy-military-records-of-service/apply-for-the-records-of-a-deceased-serviceperson"
    PAID_SEARCH = "https://www.nationalarchives.gov.uk/contact-us/our-paid-search-service/request-a-paid-search/"
    COPIES_OF_DEATH_CERTIFICATES = (
        "https://www.gov.uk/order-copy-birth-death-marriage-certificate"
    )
    CWGC_WAR_DEAD_RECORDS = "https://www.cwgc.org/find-records/find-war-dead/"
    PRIVACY_NOTICE = "https://www.nationalarchives.gov.uk/legal/privacy-policy/"
    ANCESTRY_SEARCH = "https://www.ancestry.co.uk/search/"
    FOI_REQUEST_GUIDANCE = "https://www.gov.uk/make-a-freedom-of-information-request"


class BoundaryYears(Enum):
    EARLIEST_BIRTH_YEAR = 1800
    YEAR_FROM_WHICH_PROOF_OF_DEATH_IS_REQUIRED = 1910
    LATEST_BIRTH_YEAR = 1939


@lru_cache(maxsize=1)
def get_country_choices():
    """
    Fetches country choices from the Record Copying Service API.
    Caches the result to avoid repeated API calls.
    Returns a list of country names sorted alphabetically.
    If the API call fails, returns a default list with "United Kingdom" only.
    """
    try:
        response = requests.get(current_app.config.get("COUNTRY_API_URL"), timeout=5)
        response.raise_for_status()
        countries_data = response.json()

        if countries_data:
            country_names = [country["Description"] for country in countries_data]
            return sorted(country_names)
    except Exception:
        current_app.logger.error(
            "Failed to fetch country choices from the API. Using default."
        )

    return ["United Kingdom"]
