from app.constants import MultiPageFormRoutes, BoundaryYears
from app.lib.aws import upload_proof_of_death
from flask import current_app
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

    def get_form_field_data(self, form, field_name):
        """Helper method to get the data for a specific field from the form with error handling."""
        try:
            return getattr(form, field_name).data
        except AttributeError:
            current_app.logger.error(
                f"Form ({form}) does not have field '{field_name}'"
            )
            return None

    def set_form_field_data(self, form, field_name, value):
        """Helper method to set the data for a specific field in the form with error handling."""
        try:
            form_field = getattr(form, field_name)
            form_field.data = value
        except AttributeError:
            current_app.logger.error(
                f"Form ({form}) does not have field '{field_name}'"
            )

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

    how_we_process_requests_form = State(
        enter="entering_how_we_process_requests_form", final=True
    )

    you_may_want_to_check_ancestry_page = State(
        enter="entering_you_may_want_to_check_ancestry_page", final=True
    )

    before_you_start_form = State(enter="entering_before_you_start_form", final=True)
    you_have_cancelled_your_request_page = State(
        enter="entering_you_have_cancelled_your_request_page", final=True
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

    we_do_not_have_royal_navy_service_records_form = State(
        enter="entering_we_do_not_have_royal_navy_service_records_form", final=True
    )

    we_are_unlikely_to_hold_officer_records__army_page = State(
        enter="entering_we_are_unlikely_to_hold_officer_records__army_page", final=True
    )

    we_are_unlikely_to_hold_officer_records__raf_page = State(
        enter="entering_we_are_unlikely_to_hold_officer_records__raf_page", final=True
    )

    we_are_unlikely_to_hold_officer_records__generic_page = State(
        enter="entering_we_are_unlikely_to_hold_officer_records__generic_page",
        final=True,
    )

    we_are_unlikely_to_locate_this_record_form = State(
        enter="entering_we_are_unlikely_to_locate_this_record_form", final=True
    )

    we_may_hold_this_record_page = State(
        enter="entering_we_may_hold_this_record_page", final=True
    )

    what_was_their_date_of_birth_form = State(
        enter="entering_what_was_their_date_of_birth_form", final=True
    )

    are_you_sure_you_want_to_cancel_form = State(
        enter="entering_are_you_sure_you_want_to_cancel_form", final=True
    )

    service_person_details_form = State(
        enter="entering_service_person_details_form", final=True
    )

    we_do_not_have_records_for_people_born_after_page = State(
        enter="entering_we_do_not_have_records_for_people_born_after_page", final=True
    )

    provide_a_proof_of_death_form = State(
        enter="entering_provide_a_proof_of_death_form", final=True
    )

    upload_a_proof_of_death_form = State(
        enter="entering_upload_a_proof_of_death_form", final=True
    )

    are_you_sure_you_want_to_proceed_without_proof_of_death_form = State(
        enter="entering_are_you_sure_you_want_to_proceed_without_proof_of_death_form",
        final=True,
    )

    have_you_previously_made_a_request_form = State(
        enter="entering_have_you_previously_made_a_request_form", final=True
    )

    your_contact_details_form = State(
        enter="entering_your_contact_details_form", final=True
    )

    what_is_your_address_form = State(
        enter="entering_what_is_your_address_form", final=True
    )

    choose_your_order_type_form = State(
        enter="entering_choose_your_order_type_form", final=True
    )

    your_order_summary_form = State(
        enter="entering_your_order_summary_form", final=True
    )

    gov_uk_pay_redirect = State(enter="entering_gov_uk_pay_redirect", final=True)

    request_submitted_page = State(enter="entering_request_submitted_page", final=True)

    """
    These are our Events. They're called in route methods to trigger transitions between States.

    In some cases, there will be a straightforward 1:1 mapping between states. In others, we pass a function (cond)
    that act as predicates that resolve to a boolean
    """

    continue_from_start_form = initial.to(how_we_process_requests_form)

    continue_from_how_we_process_requests_form = initial.to(before_you_start_form)

    continue_from_before_you_start_form = initial.to(
        you_may_want_to_check_ancestry_page
    )

    continue_from_are_you_sure_you_want_to_cancel_form = initial.to(
        you_have_cancelled_your_request_page
    )

    continue_from_you_may_want_to_check_ancestry_form = initial.to(
        service_person_alive_form
    )

    continue_from_service_person_alive_form = initial.to(
        subject_access_request_page, cond="living_subject"
    ) | initial.to(service_branch_form, unless="living_subject")

    continue_from_submit_subject_access_request_form = initial.to(
        are_you_sure_you_want_to_cancel_form
    )

    continue_from_service_branch_form = (
        initial.to(
            were_they_a_commissioned_officer_form,
            unless="is_royal_navy or likely_unfindable",
        )
        | initial.to(
            we_do_not_have_royal_navy_service_records_form, cond="is_royal_navy"
        )
        | initial.to(
            we_are_unlikely_to_locate_this_record_form, cond="likely_unfindable"
        )
    )

    continue_from_were_they_a_commissioned_officer_form = (
        initial.to(we_may_hold_this_record_page, unless="was_officer")
        | initial.to(
            we_are_unlikely_to_hold_officer_records__raf_page,
            cond="was_officer and service_branch_is_raf",
        )
        | initial.to(
            we_are_unlikely_to_hold_officer_records__generic_page,
            cond="was_officer and service_branch_is_other",
        )
        | initial.to(
            we_are_unlikely_to_hold_officer_records__generic_page,
            cond="was_officer and service_branch_is_unknown",
        )
        | initial.to(
            we_are_unlikely_to_hold_officer_records__army_page,
            cond="was_officer and service_branch_is_army",
        )
    )

    continue_from_we_do_not_have_royal_navy_service_records_form = initial.to(
        are_you_sure_you_want_to_cancel_form
    )

    continue_from_we_are_unlikely_to_locate_this_record_form = initial.to(
        are_you_sure_you_want_to_cancel_form
    )

    continue_from_we_may_hold_this_record_form = initial.to(
        what_was_their_date_of_birth_form
    )

    continue_from_we_are_unlikely_to_hold_officer_records_form = initial.to(
        what_was_their_date_of_birth_form
    )

    continue_from_what_was_their_date_of_birth_form = (
        initial.to(
            service_person_details_form,
            unless="born_too_late or birth_year_requires_proof_of_death",
        )
        | initial.to(
            we_do_not_have_records_for_people_born_after_page, cond="born_too_late"
        )
        | initial.to(
            provide_a_proof_of_death_form, cond="birth_year_requires_proof_of_death"
        )
    )

    continue_from_we_do_not_have_records_for_people_born_after_form = initial.to(
        are_you_sure_you_want_to_cancel_form
    )

    continue_from_provide_a_proof_of_death_form = initial.to(
        upload_a_proof_of_death_form, unless="does_not_have_proof_of_death"
    ) | initial.to(are_you_sure_you_want_to_proceed_without_proof_of_death_form)

    continue_from_are_you_sure_you_want_to_proceed_without_proof_of_death_form = (
        initial.to(
            upload_a_proof_of_death_form,
            unless="happy_to_proceed_without_proof_of_death",
        )
        | initial.to(service_person_details_form)
    )

    continue_from_upload_a_proof_of_death_form = (
        initial.to(
            service_person_details_form, cond="user_has_not_uploaded_proof_of_death"
        )
        | initial.to(service_person_details_form, cond="proof_of_death_uploaded_to_s3")
        | initial.to(upload_a_proof_of_death_form)
    )

    continue_from_service_person_details_form = initial.to(
        have_you_previously_made_a_request_form
    )

    continue_from_have_you_previously_made_a_request_form = initial.to(
        choose_your_order_type_form
    )

    continue_from_your_contact_details_form = initial.to(
        what_is_your_address_form, cond="does_not_have_email"
    ) | initial.to(your_order_summary_form)

    continue_from_what_is_your_address_form = initial.to(your_order_summary_form)

    continue_from_choose_your_order_type_form = initial.to(your_contact_details_form)

    continue_from_your_order_summary_form = initial.to(gov_uk_pay_redirect)

    continue_on_return_from_gov_uk_redirect = initial.to(request_submitted_page)

    def entering_how_we_process_requests_form(self):
        self.route_for_current_state = MultiPageFormRoutes.HOW_WE_PROCESS_REQUESTS.value

    def entering_before_you_start_form(self):
        self.route_for_current_state = MultiPageFormRoutes.BEFORE_YOU_START.value

    def entering_you_may_want_to_check_ancestry_page(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.YOU_MAY_WANT_TO_CHECK_ANCESTRY.value
        )

    def entering_you_have_cancelled_your_request_page(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.YOU_HAVE_CANCELLED_YOUR_REQUEST.value
        )

    def entering_service_person_alive_form(self):
        self.route_for_current_state = MultiPageFormRoutes.IS_SERVICE_PERSON_ALIVE.value

    def entering_subject_access_request_page(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.MUST_SUBMIT_SUBJECT_ACCESS_REQUEST.value
        )

    def entering_service_branch_form(self):
        self.route_for_current_state = MultiPageFormRoutes.SERVICE_BRANCH_FORM.value

    def entering_only_living_subjects_can_request_their_record_page(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.ONLY_LIVING_SUBJECTS_CAN_REQUEST_THEIR_RECORD.value
        )

    def entering_were_they_a_commissioned_officer_form(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.WERE_THEY_A_COMMISSIONED_OFFICER_FORM.value
        )

    def entering_we_do_not_have_royal_navy_service_records_form(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS.value
        )

    def entering_we_are_unlikely_to_hold_officer_records__army_page(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY.value
        )

    def entering_we_are_unlikely_to_hold_officer_records__raf_page(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF.value
        )

    def entering_we_are_unlikely_to_hold_officer_records__generic_page(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__GENERIC.value
        )

    def entering_we_are_unlikely_to_locate_this_record_form(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.WE_ARE_UNLIKELY_TO_LOCATE_THIS_RECORD.value
        )

    def entering_we_may_hold_this_record_page(self):
        self.route_for_current_state = MultiPageFormRoutes.WE_MAY_HOLD_THIS_RECORD.value

    def entering_what_was_their_date_of_birth_form(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.WHAT_WAS_THEIR_DATE_OF_BIRTH.value
        )

    def entering_are_you_sure_you_want_to_proceed_without_proof_of_death_form(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_PROCEED_WITHOUT_PROOF_OF_DEATH.value
        )

    def entering_are_you_sure_you_want_to_cancel_form(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_CANCEL.value
        )

    def entering_service_person_details_form(self):
        self.route_for_current_state = MultiPageFormRoutes.SERVICE_PERSON_DETAILS.value

    def entering_we_do_not_have_records_for_people_born_after_page(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_AFTER.value
        )

    def entering_provide_a_proof_of_death_form(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.PROVIDE_A_PROOF_OF_DEATH.value
        )

    def entering_upload_a_proof_of_death_form(self):
        self.route_for_current_state = MultiPageFormRoutes.UPLOAD_A_PROOF_OF_DEATH.value

    def entering_have_you_previously_made_a_request_form(self):
        self.route_for_current_state = (
            MultiPageFormRoutes.HAVE_YOU_PREVIOUSLY_MADE_A_REQUEST.value
        )

    def entering_your_contact_details_form(self):
        self.route_for_current_state = MultiPageFormRoutes.YOUR_CONTACT_DETAILS.value

    def entering_what_is_your_address_form(self):
        self.route_for_current_state = MultiPageFormRoutes.WHAT_IS_YOUR_ADDRESS.value

    def entering_choose_your_order_type_form(self):
        self.route_for_current_state = MultiPageFormRoutes.CHOOSE_YOUR_ORDER_TYPE.value

    def entering_your_order_summary_form(self):
        self.route_for_current_state = MultiPageFormRoutes.YOUR_ORDER_SUMMARY.value

    def entering_gov_uk_pay_redirect(self):
        self.route_for_current_state = MultiPageFormRoutes.SEND_TO_GOV_UK_PAY.value

    def entering_request_submitted_page(self):
        self.route_for_current_state = MultiPageFormRoutes.REQUEST_SUBMITTED.value

    def living_subject(self, form):
        """Condition method to determine if the service person is alive."""
        return self.get_form_field_data(form, "is_service_person_alive") == "yes"

    def is_royal_navy(self, form):
        """Condition method to determine if the service branch is Royal Navy."""
        return form.service_branch.data in ["ROYAL_NAVY"]

    def likely_unfindable(self, form):
        """Condition method to determine if we may be unable to find the record."""
        return self.get_form_field_data(form, "service_branch") in ["HOME_GUARD"]

    def was_officer(self, form):
        """Condition method to determine if the service person was an officer."""
        return form.were_they_a_commissioned_officer.data == "yes"

    def service_branch_is_army(self, form):
        """Condition method to determine if the service branch is British Army."""
        return form.service_branch.data == "BRITISH_ARMY"

    def service_branch_is_raf(self, form):
        """Condition method to determine if the service branch is Royal Air Force."""
        return form.service_branch.data == "ROYAL_AIR_FORCE"

    def service_branch_is_other(self, form):
        """Condition method to determine if the service branch is Other."""
        return form.service_branch.data == "OTHER"

    def service_branch_is_unknown(self, form):
        """Condition method to determine if the service branch is Unknown."""
        return form.service_branch.data == "UNKNOWN"

    def born_too_late(self, form):
        """Condition method to determine if the service person's date of birth is too late for TNA to have record."""
        return form.date_of_birth.data.year > BoundaryYears.LATEST_BIRTH_YEAR.value

    def birth_year_requires_proof_of_death(self, form):
        """Condition method to determine if the service person's date of birth requires a proof of death."""
        return (
            form.date_of_birth.data.year
            > BoundaryYears.YEAR_FROM_WHICH_PROOF_OF_DEATH_IS_REQUIRED.value
        )

    def does_not_have_email(self, form):
        """Condition method to determine if the user does not have an email address."""
        return form.does_not_have_email.data

    def does_not_have_proof_of_death(self, form):
        """Condition method to determine if the user does not have a proof of death."""
        return form.do_you_have_a_proof_of_death.data == "no"

    def happy_to_proceed_without_proof_of_death(self, form):
        """Condition method to determine if the user is happy to proceed without a proof of death."""
        return (
            form.are_you_sure_you_want_to_proceed_without_proof_of_death.data == "yes"
        )

    def user_has_not_uploaded_proof_of_death(self, form):
        """Condition method to determine if no proof of death was uploaded."""
        return not form.proof_of_death.data

    def proof_of_death_uploaded_to_s3(self, form):
        """Condition method to determine if proof of death was successfully uploaded to S3."""
        if file_data := self.get_form_field_data(form, "proof_of_death"):
            file = upload_proof_of_death(file=file_data)
            if file:
                self.set_form_field_data(form, "proof_of_death", file)
                return True
        self.set_form_field_data(form, "proof_of_death", None)
        return False  # TODO: Does this need to be True if upload fails? They won't progress otherwise.
