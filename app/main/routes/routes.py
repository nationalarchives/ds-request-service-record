from app.lib.content import load_content
from app.lib.decorators.state_machine_decorator import with_state_machine
from app.lib.decorators.with_form_prefilled_from_session import (
    with_form_prefilled_from_session,
)
from app.lib.save_catalogue_reference_to_session import (
    save_catalogue_reference_to_session,
)
from app.lib.save_submitted_form_fields_to_session import (
    save_submitted_form_fields_to_session,
)
from app.main import bp
from app.main.forms.are_you_sure_you_want_to_cancel import AreYouSureYouWantToCancel
from app.main.forms.before_you_start import BeforeYouStart
from app.main.forms.check_ancestry import CheckAncestry
from app.main.forms.do_you_have_a_proof_of_death import DoYouHaveAProofOfDeath
from app.main.forms.have_you_checked_the_catalogue import HaveYouCheckedTheCatalogue
from app.main.forms.have_you_previously_made_a_request import (
    HaveYouPreviouslyMadeARequest,
)
from app.main.forms.how_do_you_want_your_order_processed import (
    HowDoYouWantYourOrderProcessed,
)
from app.main.forms.how_the_process_works import HowTheProcessWorks
from app.main.forms.is_service_person_alive import IsServicePersonAlive
from app.main.forms.service_branch import ServiceBranch
from app.main.forms.service_person_details import ServicePersonDetails
from app.main.forms.start_now import StartNow
from app.main.forms.upload_a_proof_of_death import UploadAProofOfDeath
from app.main.forms.we_may_hold_this_record import WeMayHoldThisRecord
from app.main.forms.were_they_a_commissioned_officer import WasServicePersonAnOfficer
from app.main.forms.what_was_their_date_of_birth import WhatWasTheirDateOfBirth
from app.main.forms.your_details import YourDetails
from app.main.forms.your_postal_address import YourPostalAddress
from flask import redirect, render_template, request, url_for


@bp.route("/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(StartNow)
def start(form, state_machine):
    save_catalogue_reference_to_session(request)
    if form.validate_on_submit():
        state_machine.continue_from_start_form()
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template("main/start.html", form=form, content=load_content())


@bp.route("/how-the-process-works/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(HowTheProcessWorks)
def how_the_process_works(form, state_machine):
    if form.validate_on_submit():
        state_machine.continue_from_how_the_process_works_form()
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/how-the-process-works.html", form=form, content=load_content()
    )


@bp.route("/before-you-start/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(BeforeYouStart)
def before_you_start(form, state_machine):
    if form.validate_on_submit():
        state_machine.continue_from_before_you_start_form()
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/before-you-start.html", form=form, content=load_content()
    )


@bp.route("/are-you-sure-you-want-to-cancel/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(AreYouSureYouWantToCancel)
def are_you_sure_you_want_to_cancel(form, state_machine):
    if form.validate_on_submit():
        state_machine.continue_from_are_you_sure_you_want_to_cancel_form()
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/are-you-sure-you-want-to-cancel.html", form=form, content=load_content()
    )


@bp.route("/request-cancelled/", methods=["GET"])
def request_cancelled():
    return render_template("main/request-cancelled.html", content=load_content())


@bp.route("/check-ancestry/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(CheckAncestry)
def check_ancestry(form, state_machine):
    return render_template(
        "main/check-ancestry.html",
        form=form,
        content=load_content(),
    )


@bp.route("/have-you-checked-the-catalogue/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(HaveYouCheckedTheCatalogue)
def have_you_checked_the_catalogue(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_have_you_checked_the_catalogue_form(form)
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/have-you-checked-the-catalogue.html",
        form=form,
        content=load_content(),
    )


@bp.route("/is-service-person-alive/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(IsServicePersonAlive)
def is_service_person_alive(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_service_person_alive_form(form)
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/is-service-person-alive.html",
        form=form,
        content=load_content(),
    )


@bp.route("/must-submit-subject-access/", methods=["GET"])
def must_submit_subject_access_request():
    return render_template(
        "main/must-submit-subject-access-request.html",
        content=load_content(),
    )


@bp.route("/only-living-subjects-can-request-their-record/", methods=["GET"])
def only_living_subjects_can_request_their_record():
    return render_template(
        "main/only-living-subjects-can-request-their-record.html",
        content=load_content(),
    )


@bp.route("/service-branch/", methods=["GET", "POST"])
@with_form_prefilled_from_session(ServiceBranch)
@with_state_machine
def service_branch_form(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_service_branch_form(form)
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/service-branch.html", form=form, content=load_content()
    )


@bp.route("/was-service-person-officer/", methods=["GET", "POST"])
@with_form_prefilled_from_session(WasServicePersonAnOfficer)
@with_state_machine
def were_they_a_commissioned_officer(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_were_they_a_commissioned_officer_form(form)
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/was-service-person-an-officer.html",
        form=form,
        content=load_content(),
    )


@bp.route("/search-the-catalogue/", methods=["GET"])
def search_the_catalogue():
    return render_template("main/search-the-catalogue.html", content=load_content())


@bp.route("/we-do-not-have-records-for-this-service-branch/", methods=["GET"])
def we_do_not_have_records_for_this_service_branch():
    return render_template(
        "main/we-do-not-have-records-for-this-service-branch.html",
        content=load_content(),
    )


@bp.route("/we-do-not-have-records-for-this-rank/", methods=["GET"])
def we_do_not_have_records_for_this_rank():
    return render_template(
        "main/we-do-not-have-records-for-this-rank.html",
        content=load_content(),
    )


@bp.route("/we-may-be-unable-to-find-this-record/", methods=["GET"])
def we_are_unlikely_to_find_this_record():
    return render_template(
        "main/we-may-be-unable-to-find-this-record.html",
        content=load_content(),
    )


@bp.route("/we-may-hold-this-record/", methods=["GET", "POST"])
@with_form_prefilled_from_session(WeMayHoldThisRecord)
@with_state_machine
def we_may_hold_this_record(form, state_machine):
    if form.validate_on_submit():
        state_machine.continue_from_we_may_hold_this_record_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/we-may-hold-this-record.html",
        form=form,
        content=load_content(),
    )


@bp.route("/what-was-their-date-of-birth/", methods=["GET", "POST"])
@with_form_prefilled_from_session(WhatWasTheirDateOfBirth)
@with_state_machine
def what_was_their_date_of_birth(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_what_was_their_date_of_birth_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/what-was-their-date-of-birth.html",
        form=form,
        content=load_content(),
    )


@bp.route("/we-do-not-have-records-for-people-born-before/", methods=["GET"])
def we_do_not_have_records_for_people_born_before():
    return render_template(
        "main/we-do-not-have-records-for-people-born-before.html",
        content=load_content(),
    )


@bp.route("/we-do-not-have-records-for-people-born-after/", methods=["GET"])
def we_do_not_have_records_for_people_born_after():
    return render_template(
        "main/we-do-not-have-records-for-people-born-after.html",
        content=load_content(),
    )


@bp.route("/service-person-details/", methods=["GET", "POST"])
@with_form_prefilled_from_session(ServicePersonDetails)
@with_state_machine
def service_person_details(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_service_person_details_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/service-person-details.html",
        form=form,
        content=load_content(),
    )


@bp.route("/have-you-previously-made-a-request/", methods=["GET", "POST"])
@with_form_prefilled_from_session(HaveYouPreviouslyMadeARequest)
@with_state_machine
def have_you_previously_made_a_request(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_have_you_previously_made_a_request_form(form)
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/have-you-previously-made-a-request.html",
        form=form,
        content=load_content(),
    )


@bp.route("/your-details/", methods=["GET", "POST"])
@with_form_prefilled_from_session(YourDetails)
@with_state_machine
def your_details(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_your_details_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template("main/your-details.html", form=form, content=load_content())


@bp.route("/do-you-have-a-proof-of-death/", methods=["GET", "POST"])
@with_form_prefilled_from_session(DoYouHaveAProofOfDeath)
@with_state_machine
def do_you_have_a_proof_of_death(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_do_you_have_a_proof_of_death_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/do-you-have-a-proof-of-death.html",
        form=form,
        content=load_content(),
    )


@bp.route("/your-postal-address/", methods=["GET", "POST"])
@with_form_prefilled_from_session(YourPostalAddress)
@with_state_machine
def your_postal_address(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_your_postal_address_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/your-postal-address.html",
        form=form,
        content=load_content(),
    )


@bp.route("/how-do-you-want-your-order-processed/", methods=["GET", "POST"])
@with_state_machine
def how_do_you_want_your_order_processed(state_machine):
    form = HowDoYouWantYourOrderProcessed()
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_how_do_you_want_your_order_processed_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/how-do-you-want-your-order-processed.html",
        form=form,
        content=load_content(),
    )


@bp.route("/upload-a-proof-of-death/", methods=["GET", "POST"])
@with_form_prefilled_from_session(UploadAProofOfDeath)
@with_state_machine
def upload_a_proof_of_death(form, state_machine):
    if form.validate_on_submit():
        # Note: We should probably call the API from the state machine (as part of the continue_from_* method)
        #       so that it is the state machine that decides what state the user should be in
        #       next (this is easy to extend too because we can have the state machine do different
        #       things based on different conditions - one state for the API being down, another for
        #       the upload being successful but virus scanning identifying a problem, etc.)

        #       My sense is that this will probably be best achieved a dedicated page initially, but
        #       it's for UCD to decide how best to handle this from a user experience perspective.
        #       The key point is that this is probably not best treated as validation error on the form
        #       because:
        #         1. it's not necessarily a problem with the data the user has provided
        #         2. it will likely require us to communicate next steps to the user
        state_machine.continue_from_upload_a_proof_of_death_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/upload-a-proof-of-death.html",
        form=form,
        content=load_content(),
    )


@bp.route("/request-submitted/", methods=["GET"])
def request_submitted():
    return render_template(
        "main/request-submitted.html",
        reference_number="123456",
        content=load_content(),
    )
