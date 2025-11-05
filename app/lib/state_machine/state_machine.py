from app.constants import MultiPageFormRoutes
from statemachine import State, StateMachine


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
    have_you_checked_the_catalogue_form = State(
        enter="entering_have_you_checked_the_catalogue_form", final=True
    )
    search_the_catalogue_page = State(
        enter="entering_search_the_catalogue_page", final=True
    )
    service_person_alive_form = State(
        enter="entering_service_person_alive_form", final=True
    )
    subject_access_request_page = State(
        enter="entering_subject_access_request_page", final=True
    )
    service_branch_form = State(enter="entering_service_branch_form", final=True)
    were_they_a_commissioned_officer_form = State(
        enter="entering_were_they_a_commissioned_officer_form", final=True
    )
    we_do_not_have_records_for_this_service_branch_page = State(
        enter="entering_we_do_not_have_records_for_this_service_branch", final=True
    )
    we_do_not_have_records_for_this_rank_page = State(
        enter="entering_we_do_not_have_records_for_this_rank_page", final=True
    )
    we_are_unlikely_to_find_this_record_page = State(
        enter="entering_we_are_unlikely_to_find_this_record_page", final=True
    )
    we_may_hold_this_record_page = State(
        enter="entering_we_may_hold_this_record_page", final=True
    )
    what_was_their_date_of_birth_form = State(
        enter="entering_what_was_their_date_of_birth_page", final=True
    )
    service_person_details_form = State(
        enter="entering_service_person_details_form", final=True
    )
    we_do_not_have_records_for_people_born_after_page = State(
        enter="entering_we_do_not_have_records_for_people_born_after_page", final=True
    )
    we_do_not_have_records_for_people_born_before_page = State(
        enter="entering_we_do_not_have_records_for_people_born_before_page", final=True
    )
    do_you_have_a_proof_of_death_form = State(
        enter="entering_do_you_have_a_proof_of_death_form", final=True
    )
    upload_a_proof_of_death_form = State(
        enter="entering_upload_a_proof_of_death_form", final=True
    )
    have_you_previously_made_a_request_form = State(
        enter="entering_have_you_previously_made_a_request_form", final=True
    )
    your_details_form = State(enter="entering_your_details_form", final=True)
    your_postal_address_form = State(
        enter="entering_your_postal_address_form", final=True
    )
    how_do_you_want_your_order_processed_form = State(
        enter="entering_how_do_you_want_your_order_processed_form", final=True
    )
    gov_uk_pay_redirect = State(enter="entering_gov_uk_pay_redirect", final=True)
    request_submitted_page = State(enter="entering_request_submitted_page", final=True)

    """
    These are our Events. They're called in route methods to trigger transitions between States.

    In some cases, there will be a straightforward 1:1 mapping between states. In others, we pass a function (cond)
    that act as predicates that resolve to a boolean
    """

    continue_from_start_form = initial.to(have_you_checked_the_catalogue_form)

    continue_from_have_you_checked_the_catalogue_form = initial.to(
        service_person_alive_form, cond="has_checked_catalogue"
    ) | initial.to(search_the_catalogue_page, unless="has_checked_catalogue")

    continue_from_service_person_alive_form = initial.to(
        subject_access_request_page, cond="living_subject"
    ) | initial.to(service_branch_form, unless="living_subject")
    continue_from_service_branch_form = (
        initial.to(
            were_they_a_commissioned_officer_form,
            unless="go_to_mod or likely_unfindable",
        )
        | initial.to(
            we_do_not_have_records_for_this_service_branch_page, cond="go_to_mod"
        )
        | initial.to(we_are_unlikely_to_find_this_record_page, cond="likely_unfindable")
    )

    continue_from_were_they_a_commissioned_officer_form = initial.to(
        we_may_hold_this_record_page, unless="was_officer"
    ) | initial.to(we_do_not_have_records_for_this_rank_page, cond="was_officer")

    continue_from_we_may_hold_this_record_form = initial.to(
        what_was_their_date_of_birth_form
    )

    continue_from_what_was_their_date_of_birth_form = (
        initial.to(
            service_person_details_form,
            unless="born_too_late or born_too_early or birth_year_requires_proof_of_death",
        )
        | initial.to(
            we_do_not_have_records_for_people_born_after_page, cond="born_too_late"
        )
        | initial.to(
            we_do_not_have_records_for_people_born_before_page, cond="born_too_early"
        )
        | initial.to(
            do_you_have_a_proof_of_death_form, cond="birth_year_requires_proof_of_death"
        )
    )

    continue_from_do_you_have_a_proof_of_death_form = initial.to(
        upload_a_proof_of_death_form
    )

    continue_from_upload_a_proof_of_death_form = initial.to(service_person_details_form)

    continue_from_service_person_details_form = initial.to(
        have_you_previously_made_a_request_form
    )

    continue_from_have_you_previously_made_a_request_form = initial.to(
        your_details_form
    )

    continue_from_your_details_form = initial.to(
        your_postal_address_form, cond="does_not_have_email"
    ) | initial.to(how_do_you_want_your_order_processed_form)

    continue_from_your_postal_address_form = initial.to(
        how_do_you_want_your_order_processed_form
    )

    continue_from_how_do_you_want_your_order_processed_form = initial.to(
        gov_uk_pay_redirect
    )

    continue_on_return_from_gov_uk_redirect = initial.to(request_submitted_page)

    def entering_have_you_checked_the_catalogue_form(self, event, state):
        self.route_for_current_state = (
            MultiPageFormRoutes.HAVE_YOU_CHECKED_THE_CATALOGUE.value
        )

    def entering_search_the_catalogue_page(self, event, state):
        self.route_for_current_state = MultiPageFormRoutes.SEARCH_THE_CATALOGUE.value

    def entering_service_person_alive_form(self, event, state):
        self.route_for_current_state = MultiPageFormRoutes.IS_SERVICE_PERSON_ALIVE.value

    def entering_subject_access_request_page(self, event, state):
        self.route_for_current_state = (
            MultiPageFormRoutes.MUST_SUBMIT_SUBJECT_ACCESS_REQUEST.value
        )

    def entering_service_branch_form(self, event, state):
        self.route_for_current_state = MultiPageFormRoutes.SERVICE_BRANCH_FORM.value

    def entering_only_living_subjects_can_request_their_record_page(self, event, state):
        self.route_for_current_state = (
            MultiPageFormRoutes.ONLY_LIVING_SUBJECTS_CAN_REQUEST_THEIR_RECORD.value
        )

    def entering_were_they_a_commissioned_officer_form(self, form):
        self.route_for_current_state = (
            MultiPageFormRoutes.WERE_THEY_A_COMMISSIONED_OFFICER_FORM.value
        )

    def entering_we_do_not_have_records_for_this_service_branch(self, form):
        self.route_for_current_state = (
            MultiPageFormRoutes.WE_DO_NOT_HAVE_RECORDS_FOR_THIS_SERVICE_BRANCH.value
        )

    def entering_we_do_not_have_records_for_this_rank_page(self, form):
        self.route_for_current_state = (
            MultiPageFormRoutes.WE_DO_NOT_HAVE_RECORDS_FOR_THIS_RANK.value
        )

    def entering_we_are_unlikely_to_find_this_record_page(self, form):
        self.route_for_current_state = (
            MultiPageFormRoutes.WE_ARE_UNLIKELY_TO_FIND_THIS_RECORD.value
        )

    def entering_we_may_hold_this_record_page(self, form):
        self.route_for_current_state = MultiPageFormRoutes.WE_MAY_HOLD_THIS_RECORD.value

    def entering_what_was_their_date_of_birth_page(self, form):
        self.route_for_current_state = (
            MultiPageFormRoutes.WHAT_WAS_THEIR_DATE_OF_BIRTH.value
        )

    def entering_service_person_details_form(self, form):
        self.route_for_current_state = MultiPageFormRoutes.SERVICE_PERSON_DETAILS.value

    def entering_we_do_not_have_records_for_people_born_after_page(self, form):
        self.route_for_current_state = (
            MultiPageFormRoutes.WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_AFTER.value
        )

    def entering_we_do_not_have_records_for_people_born_before_page(self, form):
        self.route_for_current_state = (
            MultiPageFormRoutes.WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_BEFORE.value
        )

    def entering_do_you_have_a_proof_of_death_form(self, form):
        self.route_for_current_state = (
            MultiPageFormRoutes.DO_YOU_HAVE_A_PROOF_OF_DEATH.value
        )

    def entering_upload_a_proof_of_death_form(self, form):
        self.route_for_current_state = MultiPageFormRoutes.UPLOAD_A_PROOF_OF_DEATH.value

    def entering_have_you_previously_made_a_request_form(self, form):
        self.route_for_current_state = (
            MultiPageFormRoutes.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST.value
        )

    def entering_your_details_form(self, form):
        self.route_for_current_state = MultiPageFormRoutes.YOUR_DETAILS.value

    def entering_your_postal_address_form(self, form):
        self.route_for_current_state = MultiPageFormRoutes.YOUR_POSTAL_ADDRESS.value

    def entering_how_do_you_want_your_order_processed_form(self, form):
        self.route_for_current_state = (
            MultiPageFormRoutes.HOW_DO_YOU_WANT_YOUR_ORDER_PROCESSED.value
        )

    def entering_gov_uk_pay_redirect(self, form):
        self.route_for_current_state = MultiPageFormRoutes.SEND_TO_GOV_PAY.value

    def entering_request_submitted_page(self):
        self.route_for_current_state = MultiPageFormRoutes.REQUEST_SUBMITTED.value

    def on_enter_state(self, event, state):
        """This method is called when entering any state."""
        print(
            f"State machine: Entering '{state.id}' state in response to '{event}' event. The next route is set to: '{self.route_for_current_state}'"
        )

    def on_exit_state(self, event, state):
        """This method is called when exiting any state."""
        self.route_for_current_state = None
        print(
            f"State machine: Exiting '{state.id}' state in response to '{event}' event."
        )

    def has_checked_catalogue(self, form):
        """Condition method to determine if the user has checked the catalogue."""
        return form.have_you_checked_the_catalogue.data == "yes"

    def living_subject(self, form):
        """Condition method to determine if the service person is alive."""
        return form.is_service_person_alive.data == "yes"

    def go_to_mod(self, form):
        """Condition method to determine if the user should be directed to the MOD."""
        return form.service_branch.data in ["ROYAL_NAVY"]

    def likely_unfindable(self, form):
        """Condition method to determine if we may be unable to find the record."""
        return form.service_branch.data in ["HOME_GUARD"]

    def was_officer(self, form):
        """Condition method to determine if the service person was an officer."""
        return form.were_they_a_commissioned_officer.data == "yes"

    def born_too_late(self, form):
        return form.what_was_their_date_of_birth.data.year > 1939

    def born_too_early(self, form):
        return form.what_was_their_date_of_birth.data.year < 1800

    def birth_year_requires_proof_of_death(self, form):
        return form.what_was_their_date_of_birth.data.year > 1910

    def does_not_have_email(self, form):
        return form.does_not_have_email.data
