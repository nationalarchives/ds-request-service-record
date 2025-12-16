import re
from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from app.constants import MultiPageFormRoutes
from app.lib.state_machine.state_machine import RoutingStateMachine


def test_all_states_have_the_expected_suffix():
    sm = RoutingStateMachine()
    for state in sm.states:
        assert re.search(
            r"(_redirect|_form|_page|initial)$", state.id
        ), f"State ID {state.id} does not end with '_form', '_page', '_redirect', or 'initial'"


def test_all_events_have_the_expected_suffix():
    sm = RoutingStateMachine()
    for event in sm.events:
        assert re.search(
            r"(_form|_page|_redirect)$", event.id
        ), f"Event ID {event.id} does not end with '_form', '_page' or '_redirect'"


def test_initial_state_has_no_route():
    sm = RoutingStateMachine()
    assert sm.current_state.id == "initial"
    assert sm.route_for_current_state is None


def test_continue_from_start_form_sets_route():
    sm = RoutingStateMachine()
    sm.continue_from_start_form()
    assert sm.current_state.id == "how_we_process_requests_form"
    assert (
        sm.route_for_current_state == MultiPageFormRoutes.HOW_WE_PROCESS_REQUESTS.value
    )


def test_continue_from_before_you_start_sets_route():
    sm = RoutingStateMachine()
    sm.continue_from_before_you_start_form()
    assert sm.current_state.id == "you_may_want_to_check_ancestry_page"
    assert (
        sm.route_for_current_state
        == MultiPageFormRoutes.YOU_MAY_WANT_TO_CHECK_ANCESTRY.value
    )


def test_continue_from_are_you_sure_you_want_to_cancel_sets_route():
    sm = RoutingStateMachine()
    sm.continue_from_are_you_sure_you_want_to_cancel_form()
    assert sm.current_state.id == "you_have_cancelled_your_request_page"
    assert (
        sm.route_for_current_state
        == MultiPageFormRoutes.YOU_HAVE_CANCELLED_YOUR_REQUEST.value
    )


def test_continue_from_you_may_want_to_check_ancestry_sets_route():
    sm = RoutingStateMachine()
    sm.continue_from_you_may_want_to_check_ancestry_form()
    assert sm.current_state.id == "service_person_alive_form"
    assert (
        sm.route_for_current_state == MultiPageFormRoutes.IS_SERVICE_PERSON_ALIVE.value
    )


@pytest.mark.parametrize(
    "answer,expected_state,expected_route",
    [
        (
            "yes",
            "subject_access_request_page",
            MultiPageFormRoutes.MUST_SUBMIT_SUBJECT_ACCESS_REQUEST.value,
        ),
        ("no", "service_branch_form", MultiPageFormRoutes.SERVICE_BRANCH_FORM.value),
        (
            "unknown",
            "service_branch_form",
            MultiPageFormRoutes.SERVICE_BRANCH_FORM.value,
        ),
    ],
)
def test_continue_from_service_person_alive_form_routes_by_condition(
    answer, expected_state, expected_route
):
    sm = RoutingStateMachine()
    sm.continue_from_service_person_alive_form(
        form=make_form(is_service_person_alive=answer)
    )
    assert sm.current_state.id == expected_state
    assert sm.route_for_current_state == expected_route


@pytest.mark.parametrize(
    "answer,expected_state,expected_route",
    [
        (
            "BRITISH_ARMY",
            "were_they_a_commissioned_officer_form",
            MultiPageFormRoutes.WERE_THEY_A_COMMISSIONED_OFFICER_FORM.value,
        ),
        (
            "ROYAL_NAVY",
            "we_do_not_have_royal_navy_service_records_form",
            MultiPageFormRoutes.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS.value,
        ),
        (
            "HOME_GUARD",
            "we_are_unlikely_to_locate_this_record_form",
            MultiPageFormRoutes.WE_ARE_UNLIKELY_TO_LOCATE_THIS_RECORD.value,
        ),
        (
            "ROYAL_AIR_FORCE",
            "were_they_a_commissioned_officer_form",
            MultiPageFormRoutes.WERE_THEY_A_COMMISSIONED_OFFICER_FORM.value,
        ),
        (
            "BRITISH_ARMY_OTHER",
            "were_they_a_commissioned_officer_form",
            MultiPageFormRoutes.WERE_THEY_A_COMMISSIONED_OFFICER_FORM.value,
        ),
        (
            "UNKNOWN",
            "were_they_a_commissioned_officer_form",
            MultiPageFormRoutes.WERE_THEY_A_COMMISSIONED_OFFICER_FORM.value,
        ),
    ],
)
def test_continue_from_service_branch_form_routes_by_condition(
    answer, expected_state, expected_route
):
    sm = RoutingStateMachine()
    sm.continue_from_service_branch_form(form=make_form(service_branch=answer))
    assert sm.current_state.id == expected_state
    assert sm.route_for_current_state == expected_route


def test_continue_from_we_do_not_have_royal_navy_service_records():
    sm = RoutingStateMachine()
    sm.continue_from_we_do_not_have_royal_navy_service_records_form()
    assert sm.current_state.id == "are_you_sure_you_want_to_cancel_form"
    assert (
        sm.route_for_current_state
        == MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_CANCEL.value
    )


def test_continue_from_we_are_unlikely_to_locate_this_record():
    sm = RoutingStateMachine()
    sm.continue_from_we_are_unlikely_to_locate_this_record_form()
    assert sm.current_state.id == "are_you_sure_you_want_to_cancel_form"
    assert (
        sm.route_for_current_state
        == MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_CANCEL.value
    )


def test_continue_from_submit_subject_access_request_form():
    sm = RoutingStateMachine()
    sm.continue_from_submit_subject_access_request_form(
        form=make_form(submit_subject_access_request=None)
    )
    assert sm.current_state.id == "are_you_sure_you_want_to_cancel_form"
    assert (
        sm.route_for_current_state
        == MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_CANCEL.value
    )


@pytest.mark.parametrize(
    "service_branch,was_officer,expected_state,expected_route",
    [
        (
            "BRITISH_ARMY",
            "no",
            "we_may_hold_this_record_page",
            MultiPageFormRoutes.WE_MAY_HOLD_THIS_RECORD.value,
        ),
        (
            "BRITISH_ARMY",
            "unknown",
            "we_may_hold_this_record_page",
            MultiPageFormRoutes.WE_MAY_HOLD_THIS_RECORD.value,
        ),
        (
            "BRITISH_ARMY",
            "yes",
            "we_are_unlikely_to_hold_officer_records__army_page",
            MultiPageFormRoutes.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY.value,
        ),
        (
            "ROYAL_AIR_FORCE",
            "yes",
            "we_are_unlikely_to_hold_officer_records__raf_page",
            MultiPageFormRoutes.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF.value,
        ),
        (
            "OTHER",
            "yes",
            "we_are_unlikely_to_hold_officer_records__generic_page",
            MultiPageFormRoutes.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__GENERIC.value,
        ),
        (
            "OTHER",
            "no",
            "we_may_hold_this_record_page",
            MultiPageFormRoutes.WE_MAY_HOLD_THIS_RECORD.value,
        ),
        (
            "OTHER",
            "unknown",
            "we_may_hold_this_record_page",
            MultiPageFormRoutes.WE_MAY_HOLD_THIS_RECORD.value,
        ),
        (
            "UNKNOWN",
            "yes",
            "we_are_unlikely_to_hold_officer_records__generic_page",
            MultiPageFormRoutes.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__GENERIC.value,
        ),
        (
            "UNKNOWN",
            "no",
            "we_may_hold_this_record_page",
            MultiPageFormRoutes.WE_MAY_HOLD_THIS_RECORD.value,
        ),
        (
            "UNKNOWN",
            "unknown",
            "we_may_hold_this_record_page",
            MultiPageFormRoutes.WE_MAY_HOLD_THIS_RECORD.value,
        ),
    ],
)
def test_continue_from_were_they_a_commissioned_officer_form_routes_by_condition(
    service_branch, was_officer, expected_state, expected_route
):
    sm = RoutingStateMachine()
    sm.continue_from_were_they_a_commissioned_officer_form(
        form=make_form(
            service_branch=service_branch, were_they_a_commissioned_officer=was_officer
        )
    )
    assert sm.current_state.id == expected_state
    assert sm.route_for_current_state == expected_route


def test_continue_from_we_may_hold_this_record():
    sm = RoutingStateMachine()
    sm.continue_from_we_may_hold_this_record_form(
        form=make_form(we_may_hold_this_record=None)
    )
    assert sm.current_state.id == "what_was_their_date_of_birth_form"
    assert (
        sm.route_for_current_state
        == MultiPageFormRoutes.WHAT_WAS_THEIR_DATE_OF_BIRTH.value
    )


def test_continue_from_we_are_unlikely_to_hold_officer_records():
    sm = RoutingStateMachine()
    sm.continue_from_we_are_unlikely_to_hold_officer_records_form(
        form=make_form(we_are_unlikely_to_hold_officer_records=None)
    )
    assert sm.current_state.id == "what_was_their_date_of_birth_form"
    assert (
        sm.route_for_current_state
        == MultiPageFormRoutes.WHAT_WAS_THEIR_DATE_OF_BIRTH.value
    )


@pytest.mark.parametrize(
    "date_of_birth,expected_state,expected_route",
    [
        (
            date(year, 1, 1),
            "we_do_not_have_records_for_people_born_after_page",
            MultiPageFormRoutes.WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_AFTER.value,
        )
        for year in range(1940, 2000)
    ]
    + [
        (
            date(year, 1, 1),
            "service_person_details_form",
            MultiPageFormRoutes.SERVICE_PERSON_DETAILS.value,
        )
        for year in range(1800, 1910)
    ]
    + [
        (
            date(year, 1, 1),
            "do_you_have_a_proof_of_death_form",
            MultiPageFormRoutes.DO_YOU_HAVE_A_PROOF_OF_DEATH.value,
        )
        for year in range(1911, 1939)
    ],
)
def test_continue_from_what_was_their_date_of_birth_form(
    date_of_birth, expected_state, expected_route
):
    sm = RoutingStateMachine()
    sm.continue_from_what_was_their_date_of_birth_form(
        form=make_form(what_was_their_date_of_birth=date_of_birth)
    )
    assert sm.current_state.id == expected_state
    assert sm.route_for_current_state == expected_route


@pytest.mark.parametrize(
    "has_proof_of_death,expected_state,expected_route",
    [
        (
            "no",
            "are_you_sure_you_want_to_proceed_without_proof_of_death_form",
            MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_PROCEED_WITHOUT_PROOF_OF_DEATH.value,
        ),
        (
            "yes",
            "upload_a_proof_of_death_form",
            MultiPageFormRoutes.UPLOAD_A_PROOF_OF_DEATH.value,
        ),
    ],
)
def test_continue_from_do_you_have_a_proof_of_death(
    has_proof_of_death, expected_state, expected_route
):
    sm = RoutingStateMachine()
    sm.continue_from_do_you_have_a_proof_of_death_form(
        form=make_form(do_you_have_a_proof_of_death=has_proof_of_death)
    )
    assert sm.current_state.id == expected_state
    assert sm.route_for_current_state == expected_route


@pytest.mark.parametrize(
    "selection,expected_state,expected_route",
    [
        (
            "yes",
            "service_person_details_form",
            MultiPageFormRoutes.SERVICE_PERSON_DETAILS.value,
        ),
        (
            "no",
            "upload_a_proof_of_death_form",
            MultiPageFormRoutes.UPLOAD_A_PROOF_OF_DEATH.value,
        ),
    ],
)
def test_continue_from_are_you_sure_you_want_to_proceed_without_proof_of_death(
    selection, expected_state, expected_route
):
    sm = RoutingStateMachine()
    sm.continue_from_are_you_sure_you_want_to_proceed_without_proof_of_death_form(
        form=make_form(
            are_you_sure_you_want_to_proceed_without_proof_of_death=selection
        )
    )
    assert sm.current_state.id == expected_state
    assert sm.route_for_current_state == expected_route


def test_continue_from_we_do_not_have_records_for_people_born_after_form():
    sm = RoutingStateMachine()
    sm.continue_from_we_do_not_have_records_for_people_born_after_form()
    assert sm.current_state.id == "are_you_sure_you_want_to_cancel_form"
    assert (
        sm.route_for_current_state
        == MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_CANCEL.value
    )


# In the real world, upload_proof_of_death interacts with AWS S3, so we mock it here. In this case
# we test the scenario where it returns None, simulating a failed upload.
@patch("app.lib.state_machine.state_machine.upload_proof_of_death", return_value=None)
def test_continue_from_upload_a_proof_of_death_where_upload_proof_of_death_returns_none(
    mock_upload,
):
    sm = RoutingStateMachine()
    sm.continue_from_upload_a_proof_of_death_form(
        form=make_form(proof_of_death="an-uploaded-file-object")
    )
    assert sm.current_state.id == "upload_a_proof_of_death_form"
    assert sm.route_for_current_state == "main.upload_a_proof_of_death"


# In this test we are again mocking upload_proof_of_death, but this time we simulate a successful
# upload by having it return a filename.
@patch(
    "app.lib.state_machine.state_machine.upload_proof_of_death",
    return_value="filename_on_s3",
)
def test_continue_from_upload_a_proof_of_death_where_upload_proof_of_death_returns_a_filename(
    mock_upload,
):
    sm = RoutingStateMachine()
    sm.continue_from_upload_a_proof_of_death_form(
        form=make_form(proof_of_death="an-uploaded-file-object")
    )
    assert sm.current_state.id == "service_person_details_form"
    assert sm.route_for_current_state == "main.service_person_details"


# In this case we are again testing sm.continue_from_upload_a_proof_of_death_form but there is no
# need to mock upload_proof_of_death as the form's proof_of_death field is None, simulating
# the user not uploading a file (e.g. they submitted the form without selecting a file).
def test_continue_from_upload_a_proof_of_death_where_proof_of_death_is_not_provided():
    sm = RoutingStateMachine()
    sm.continue_from_upload_a_proof_of_death_form(form=make_form(proof_of_death=None))
    assert sm.current_state.id == "service_person_details_form"
    assert sm.route_for_current_state == "main.service_person_details"


def test_continue_from_service_person_details():
    sm = RoutingStateMachine()
    sm.continue_from_service_person_details_form(
        form=make_form(service_person_details=None)
    )
    assert sm.current_state.id == "have_you_previously_made_a_request_form"
    assert (
        sm.route_for_current_state
        == MultiPageFormRoutes.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST.value
    )


def test_continue_from_have_you_previously_made_a_request():
    sm = RoutingStateMachine()

    sm.continue_from_have_you_previously_made_a_request_form(
        form=make_form(
            forenames=None,
            last_name=None,
            place_of_birth=None,
            date_of_death=None,
            died_in_service=None,
            service_number=None,
            regiment=None,
            additional_information=None,
            submit=None,
        )
    )


@pytest.mark.parametrize(
    "does_not_have_email,current_state_id,route_for_current_state",
    [
        (
            True,
            "what_is_your_address_form",
            MultiPageFormRoutes.WHAT_IS_YOUR_ADDRESS.value,
        ),
        (
            False,
            "your_order_summary_form",
            MultiPageFormRoutes.YOUR_ORDER_SUMMARY.value,
        ),
    ],
)
def test_continue_from_your_contact_details(
    does_not_have_email, current_state_id, route_for_current_state
):
    sm = RoutingStateMachine()
    sm.continue_from_your_contact_details_form(
        form=make_form(
            requester_first_name=None,
            requester_last_name=None,
            does_not_have_email=does_not_have_email,
            requester_email=None,
            submit=None,
        )
    )
    assert sm.current_state.id == current_state_id
    assert sm.route_for_current_state == route_for_current_state


def test_continue_from_what_is_your_address():
    sm = RoutingStateMachine()
    sm.continue_from_what_is_your_address_form(
        form=make_form(
            address_line_1=None,
            address_line_2=None,
            address_line_3=None,
            town_or_city=None,
            county=None,
            postcode=None,
            country=None,
            submit=None,
        )
    )
    assert sm.current_state.id == "your_order_summary_form"
    assert sm.route_for_current_state == MultiPageFormRoutes.YOUR_ORDER_SUMMARY.value


@pytest.mark.parametrize("processing_option", ["standard", "full"])
def test_continue_from_choose_your_order_type(processing_option):
    sm = RoutingStateMachine()
    sm.continue_from_choose_your_order_type_form(
        form=make_form(
            processing_option=processing_option,
            choose_your_order_type_standard=None,
            choose_your_order_type_full=None,
            submit=None,
        )
    )
    assert sm.current_state.id == "your_contact_details_form"
    assert sm.route_for_current_state == MultiPageFormRoutes.YOUR_CONTACT_DETAILS.value


def test_continue_from_your_order_summary():
    sm = RoutingStateMachine()
    sm.continue_from_your_order_summary_form(form=make_form(submit=None))
    assert sm.current_state.id == "gov_uk_pay_redirect"
    assert sm.route_for_current_state == MultiPageFormRoutes.SEND_TO_GOV_UK_PAY.value


def test_continue_from_gov_uk_pay():
    sm = RoutingStateMachine()
    sm.continue_on_return_from_gov_uk_redirect()
    assert sm.current_state.id == "request_submitted_page"
    assert sm.route_for_current_state == MultiPageFormRoutes.REQUEST_SUBMITTED.value


def make_form(**fields):
    return SimpleNamespace(**{k: SimpleNamespace(data=v) for k, v in fields.items()})
