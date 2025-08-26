from statemachine import StateMachine, State


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
    """
    These are our Events. We call these in route methods to trigger transitions between States.

    Be very careful with naming to ensure they are described as an Event.
    For example, "continue_to_service_person_alive_form" is an Event that triggers a transition
    from the "start" State to the "service_person_alive_form" State.
    """
    continue_to_service_person_alive_form = initial.to(service_person_alive_form)
    continue_from_service_person_alive_form = (
        initial.to(subject_access_request_statement, cond="living_subject")
        | initial.to(service_branch_form, unless="living_subject")
    )

    def entering_service_person_alive_form(self, event, state):
        self.route_for_current_state = "main.is_service_person_alive"

    def entering_subject_access_request_statement(self, event, state):
        self.route_for_current_state = "main.must_submit_subject_access_request"

    def entering_service_branch_form(self, event, state):
        self.route_for_current_state = "main.service_branch_form"

    def on_enter_state(self, event, state):
        """This method is called when entering any state."""
        print(f"State machine: Entering '{state.id}' state in response to '{event}' event. The next route is set to: '{self.route_for_current_state}'")

    def on_exit_state(self, event, state):
        """This method is called when exiting any state."""
        self.route_for_current_state = None
        print(f"State machine: Exiting '{state.id}' state in response to '{event}' event.")

    def living_subject(self, form):
        """Condition method to determine if the service person is alive."""
        return form.is_service_person_alive.data == "yes"
