from statemachine import StateMachine, State
from app.constants import MultiPageFormRoutes


class RoutingStateMachine(StateMachine):
    """
    _route_for_current_state is updated by entering_* methods. to hold the route associated with the current state
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
    These are our States. They represent the different stages of the user journey. In most cases, you
    can think of a state as representing a form or page being presented to the user.

    The 'enter' parameter is the method called when entering the state. We use these to set the route
    for the current state. 
    
    Naming can be important for us humans when working with state machines, because it can be difficult
    to tell if something is a state or a transition. What I've tried to do here is use the convention of 
    appending either "_form" or "_page" to the end of all states. 

    """
    initial = State(initial=True)  # The initial state of our machine
    service_person_alive_form = State(enter="entering_service_person_alive_form", final=True)
    subject_access_request_page = State(enter="entering_subject_access_request_page", final=True)
    service_branch_form = State(enter="entering_service_branch_form", final=True)
    only_living_subjects_can_request_their_record_page = State(
        enter="entering_only_living_subjects_can_request_their_record_page", final=True)
    was_service_person_officer_form = State(enter="entering_was_service_person_officer_form", final=True)
    mod_have_this_record_page = State(enter="entering_mod_have_this_record", final=True)
    check_ancestry_page = State(enter="entering_check_ancestry_page", final=True)
    """
    These are our Events. They're called in route methods to trigger transitions between States.

    In some cases, there will be a straightforward 1:1 mapping between states. In others, we pass a function (cond)
    that act as predicates that resolve to a boolean
    """
    continue_to_service_person_alive_form = initial.to(service_person_alive_form)
    continue_from_service_person_alive_form = (
            initial.to(subject_access_request_page, cond="living_subject")
            | initial.to(service_branch_form, cond="deceased_subject")
            | initial.to(only_living_subjects_can_request_their_record_page, cond="potentially_living_subject")
    )
    continue_from_service_branch_form = (
            initial.to(was_service_person_officer_form, unless="go_to_mod or check_ancestry")
            | initial.to(mod_have_this_record_page, cond="go_to_mod")
            | initial.to(check_ancestry_page, cond="check_ancestry")
    )

    def entering_service_person_alive_form(self, event, state):
        self.route_for_current_state = MultiPageFormRoutes.IS_SERVICE_PERSON_ALIVE.value

    def entering_subject_access_request_page(self, event, state):
        self.route_for_current_state = MultiPageFormRoutes.MUST_SUBMIT_SUBJECT_ACCESS_REQUEST.value

    def entering_service_branch_form(self, event, state):
        self.route_for_current_state = MultiPageFormRoutes.SERVICE_BRANCH_FORM.value

    def entering_only_living_subjects_can_request_their_record_page(self, event, state):
        self.route_for_current_state = MultiPageFormRoutes.ONLY_LIVING_SUBJECTS_CAN_REQUEST_THEIR_RECORD.value

    def entering_was_service_person_officer_form(self, form):
        self.route_for_current_state = MultiPageFormRoutes.WAS_SERVICE_PERSON_OFFICER_FORM.value

    def entering_mod_have_this_record(self, form):
        self.route_for_current_state = MultiPageFormRoutes.MOD_HAVE_THIS_RECORD.value

    def entering_check_ancestry_page(self, form):
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
