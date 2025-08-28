from statemachine import StateMachine, State
from app.constants import MultiPageFormRoutes


class RoutingStateMachine(StateMachine):
    """
    _route_for_current_state is updated by entering_* methods to indicate the route to be used for the current state
    It is then used by the route handlers to redirect to the correct page after a state transition
    """
    _route_for_current_state = None

    @property
    def route_for_current_state(self):
        return self._route_for_current_state

    @route_for_current_state.setter
    def route_for_current_state(self, value):
        self._route_for_current_state = value

    """
    These are our States. They represent the different stages of our process.

    We call callbacks when entering these States to set the attributes that will be used
    in the route methods.

    Be very careful with naming to ensure they are described a State, not an Event. 
    For example, "service_person_alive_form" is a State, while "continue_to_service_person_alive_form" 
    would be an Event that triggers a transition to that State. 
    """
    initial = State(initial=True)  # The initial state of our machine
    service_person_alive_form = State(enter="entering_service_person_alive_form", final=True)
    subject_access_request_statement = State(enter="entering_subject_access_request_statement", final=True)
    service_branch_form = State(enter="entering_service_branch_form", final=True)
    only_living_subjects_can_request_their_record_statement = State(
        enter="entering_only_living_subjects_can_request_their_record_statement", final=True)
    was_service_person_officer_form = State(enter="entering_was_service_person_officer_form", final=True)
    mod_have_this_record_statement = State(enter="entering_mod_have_this_record", final=True)
    check_ancestry_statement = State(enter="entering_check_ancestry_statement", final=True)
    """
    These are our Events. We call these in route methods to trigger transitions between States.

    Be very careful with naming to ensure they are described as an Event.
    For example, "continue_to_service_person_alive_form" is an Event that triggers a transition
    from the "start" State to the "service_person_alive_form" State.
    """
    continue_to_service_person_alive_form = initial.to(service_person_alive_form)
    continue_from_service_person_alive_form = (
            initial.to(subject_access_request_statement, cond="living_subject")
            | initial.to(service_branch_form, cond="deceased_subject")
            | initial.to(only_living_subjects_can_request_their_record_statement, cond="potentially_living_subject")
    )
    continue_from_service_branch_form = (
            initial.to(was_service_person_officer_form, unless="go_to_mod or check_ancestry")
            | initial.to(mod_have_this_record_statement, cond="go_to_mod")
            | initial.to(check_ancestry_statement, cond="check_ancestry")
    )

    def entering_service_person_alive_form(self, event, state):
        self.route_for_current_state = MultiPageFormRoutes.IS_SERVICE_PERSON_ALIVE.value

    def entering_subject_access_request_statement(self, event, state):
        self.route_for_current_state = MultiPageFormRoutes.MUST_SUBMIT_SUBJECT_ACCESS_REQUEST.value

    def entering_service_branch_form(self, event, state):
        self.route_for_current_state = MultiPageFormRoutes.SERVICE_BRANCH_FORM.value

    def entering_only_living_subjects_can_request_their_record_statement(self, event, state):
        self.route_for_current_state = MultiPageFormRoutes.ONLY_LIVING_SUBJECTS_CAN_REQUEST_THEIR_RECORD.value

    def entering_was_service_person_officer_form(self, form):
        self.route_for_current_state = MultiPageFormRoutes.WAS_SERVICE_PERSON_OFFICER_FORM.value

    def entering_mod_have_this_record(self, form):
        self.route_for_current_state = MultiPageFormRoutes.MOD_HAVE_THIS_RECORD.value

    def entering_check_ancestry_statement(self, form):
        self.route_for_current_state = MultiPageFormRoutes.CHECK_ANCESTRY.value

    def on_enter_state(self, event, state):
        """This method is called when entering any state."""
        print(
            f"State machine: Entering '{state.id}' state in response to '{event}' event. The next route is set to: '{self.route_for_current_state}'")

    def on_exit_state(self, event, state):
        """This method is called when exiting any state."""
        self.route_for_current_state = None
        print(f"State machine: Exiting '{state.id}' state in response to '{event}' event.")

    def living_subject(self, form):
        """Condition method to determine if the service person is alive."""
        return form.is_service_person_alive.data == "yes"

    def go_to_mod(self, form):
        """Condition method to determine if the user should be directed to the MOD."""
        return form.service_branch.data in ["ROYAL_NAVY"]

    def check_ancestry(self, form):
        """Condition method to determine if the user should be directed to the check Ancestry."""
        return form.service_branch.data in ["HOME_GUARD"]

    def deceased_subject(self, form):
        """Condition method to determine if the service person is deceased."""
        return form.is_service_person_alive.data == "no"

    def potentially_living_subject(self, form):
        """Condition method to determine if the service person is potentially living."""
        return form.is_service_person_alive.data == "unsure"
