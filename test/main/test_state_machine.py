import pytest
from types import SimpleNamespace
from app.constants import MultiPageFormRoutes
from app.lib.state_machine.state_machine import RoutingStateMachine


def test_initial_state_has_no_route():
    sm = RoutingStateMachine()
    assert sm.current_state.id == "initial"
    assert sm.route_for_current_state is None


def test_continue_to_have_you_checked_the_catalogue_form_sets_route():
    sm = RoutingStateMachine()
    sm.continue_to_have_you_checked_the_catalogue_form()
    assert sm.current_state.id == "have_you_checked_the_catalogue_form"
    assert (
        sm.route_for_current_state
        == MultiPageFormRoutes.HAVE_YOU_CHECKED_THE_CATALOGUE.value
    )


@pytest.mark.parametrize(
    "answer,expected_state,expected_route",
    [
        (
            "yes",
            "service_person_alive_form",
            MultiPageFormRoutes.IS_SERVICE_PERSON_ALIVE.value,
        ),
        (
            "no",
            "search_the_catalogue_page",
            MultiPageFormRoutes.SEARCH_THE_CATALOGUE.value,
        ),
    ],
)
def test_continue_from_have_you_checked_the_catalogue_form_routes_by_condition(
    answer, expected_state, expected_route
):
    sm = RoutingStateMachine()
    sm.continue_from_have_you_checked_the_catalogue_form(
        form=make_form("have_you_checked_the_catalogue", answer)
    )
    assert sm.current_state.id == expected_state
    assert sm.route_for_current_state == expected_route


@pytest.mark.parametrize(
    "answer,expected_state,expected_route",
    [
        (
            "yes",
            "subject_access_request_page",
            MultiPageFormRoutes.MUST_SUBMIT_SUBJECT_ACCESS_REQUEST.value,
        ),
        ("no", "service_branch_form", MultiPageFormRoutes.SERVICE_BRANCH_FORM.value),
    ],
)
def test_continue_from_service_person_alive_form_routes_by_condition(
    answer, expected_state, expected_route
):
    sm = RoutingStateMachine()
    sm.continue_from_service_person_alive_form(
        form=make_form("is_service_person_alive", answer)
    )
    assert sm.current_state.id == expected_state
    assert sm.route_for_current_state == expected_route


@pytest.mark.parametrize(
    "answer,expected_state,expected_route",
    [
        (
            "BRITISH_ARMY",
            "was_service_person_an_officer_form",
            MultiPageFormRoutes.WAS_SERVICE_PERSON_AN_OFFICER_FORM.value,
        ),
        (
            "ROYAL_NAVY",
            "we_do_not_have_records_for_this_service_branch_page",
            MultiPageFormRoutes.WE_DO_NOT_HAVE_RECORDS_FOR_THIS_SERVICE_BRANCH.value,
        ),
        (
            "HOME_GUARD",
            "we_may_be_unable_to_find_this_record_page",
            MultiPageFormRoutes.WE_MAY_BE_UNABLE_TO_FIND_THIS_RECORD.value,
        ),
        (
            "ROYAL_AIR_FORCE",
            "was_service_person_an_officer_form",
            MultiPageFormRoutes.WAS_SERVICE_PERSON_AN_OFFICER_FORM.value,
        ),
        (
            "BRITISH_ARMY_OTHER",
            "was_service_person_an_officer_form",
            MultiPageFormRoutes.WAS_SERVICE_PERSON_AN_OFFICER_FORM.value,
        ),
        (
            "UNKNOWN",
            "was_service_person_an_officer_form",
            MultiPageFormRoutes.WAS_SERVICE_PERSON_AN_OFFICER_FORM.value,
        ),
    ],
)
def test_continue_from_service_branch_form_routes_by_condition(
    answer, expected_state, expected_route
):
    sm = RoutingStateMachine()
    sm.continue_from_service_branch_form(form=make_form("service_branch", answer))
    assert sm.current_state.id == expected_state
    assert sm.route_for_current_state == expected_route


@pytest.mark.parametrize(
    "answer,expected_state,expected_route",
    [
        (
            "no",
            "we_may_hold_this_record_page",
            MultiPageFormRoutes.WE_MAY_HOLD_THIS_RECORD.value,
        ),
        (
            "unknown",
            "we_may_hold_this_record_page",
            MultiPageFormRoutes.WE_MAY_HOLD_THIS_RECORD.value,
        ),
        (
            "yes",
            "we_do_not_have_records_for_this_rank_page",
            MultiPageFormRoutes.WE_DO_NOT_HAVE_RECORDS_FOR_THIS_RANK.value,
        ),
    ],
)
def test_continue_from_was_service_person_an_officer_form_routes_by_condition(
    answer, expected_state, expected_route
):
    sm = RoutingStateMachine()
    sm.continue_from_was_service_person_an_officer_form(
        form=make_form("was_service_person_an_officer", answer)
    )
    assert sm.current_state.id == expected_state
    assert sm.route_for_current_state == expected_route

def test_continue_from_we_may_hold_this_record():
    sm = RoutingStateMachine()
    sm.continue_from_we_may_hold_this_record_form(form=make_form("we_may_hold_this_record"))
    assert sm.current_state.id == "what_was_their_date_of_birth"
    assert (
        sm.route_for_current_state
        == MultiPageFormRoutes.WHAT_WAS_THEIR_DATE_OF_BIRTH.value
    )


def make_form(field_name: str, answer: str = None):
    return SimpleNamespace(**{field_name: SimpleNamespace(data=answer)})
