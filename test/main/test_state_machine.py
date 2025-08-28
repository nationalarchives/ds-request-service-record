import pytest
from types import SimpleNamespace
from app.constants import MultiPageFormRoutes
from app.lib.state_machine.state_machine import RoutingStateMachine


def test_initial_state_has_no_route():
    sm = RoutingStateMachine()
    assert sm.current_state.id == "initial"
    assert sm.route_for_current_state is None


def test_continue_to_service_person_alive_form_sets_route():
    sm = RoutingStateMachine()
    sm.continue_to_service_person_alive_form()
    assert sm.current_state.id == "service_person_alive_form"
    assert sm.route_for_current_state == MultiPageFormRoutes.IS_SERVICE_PERSON_ALIVE.value


@pytest.mark.parametrize(
    "answer,expected_state,expected_route",
    [
        ("yes", "subject_access_request_statement", MultiPageFormRoutes.MUST_SUBMIT_SUBJECT_ACCESS_REQUEST.value),
        ("no", "service_branch_form", MultiPageFormRoutes.SERVICE_BRANCH_FORM.value),
        ("unsure", "only_living_subjects_can_request_their_record_statement",
         MultiPageFormRoutes.ONLY_LIVING_SUBJECTS_CAN_REQUEST_THEIR_RECORD.value),
    ],
)
def test_continue_from_service_person_alive_form_routes_by_condition(answer, expected_state, expected_route):
    sm = RoutingStateMachine()
    sm.continue_from_service_person_alive_form(form=make_form(answer))
    assert sm.current_state.id == expected_state
    assert sm.route_for_current_state == expected_route


@pytest.mark.parametrize(
    "answer,expected_state,expected_route",
    [
        ("BRITISH_ARMY", "was_service_person_officer_form", MultiPageFormRoutes.WAS_SERVICE_PERSON_OFFICER_FORM.value),
        ("ROYAL_NAVY", "mod_have_this_record_statement", MultiPageFormRoutes.MOD_HAVE_THIS_RECORD.value),
        ("HOME_GUARD", "check_ancestry_statement", MultiPageFormRoutes.CHECK_ANCESTRY.value),
        ("ROYAL_AIR_FORCE", "was_service_person_officer_form",
         MultiPageFormRoutes.WAS_SERVICE_PERSON_OFFICER_FORM.value),
        ("BRITISH_ARMY_OTHER", "was_service_person_officer_form",
         MultiPageFormRoutes.WAS_SERVICE_PERSON_OFFICER_FORM.value),
        ("UNKNOWN", "was_service_person_officer_form", MultiPageFormRoutes.WAS_SERVICE_PERSON_OFFICER_FORM.value),
    ],
)
def test_continue_from_service_branch_form_routes_by_condition(answer, expected_state, expected_route):
    sm = RoutingStateMachine()
    sm.continue_from_service_branch_form(form=make_form(answer))
    assert sm.current_state.id == expected_state
    assert sm.route_for_current_state == expected_route


def make_form(answer: str):
    return SimpleNamespace(
        is_service_person_alive=SimpleNamespace(data=answer),
        service_branch=SimpleNamespace(data=answer)
    )
