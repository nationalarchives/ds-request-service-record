from app.constants import ExternalLinks, MultiPageFormRoutes
from app.lib.content import load_content
from app.lib.decorators.state_machine_decorator import with_state_machine
from app.lib.decorators.with_back_url_saved_to_session import (
    with_route_for_back_link_saved_to_session,
)
from app.lib.decorators.with_form_prefilled_from_session import (
    with_form_prefilled_from_session,
)
from app.lib.get_back_link_route import get_back_link_route
from app.lib.save_catalogue_reference_to_session import (
    save_catalogue_reference_to_session,
)
from app.lib.save_submitted_form_fields_to_session import (
    save_submitted_form_fields_to_session,
)
from app.main import bp
from app.main.forms.are_you_sure_you_want_to_cancel import AreYouSureYouWantToCancel
from app.main.forms.before_you_start import BeforeYouStart
from app.main.forms.do_you_have_a_proof_of_death import DoYouHaveAProofOfDeath
from app.main.forms.are_you_sure_you_want_to_proceed_without_proof_of_death import (
    AreYouSureYouWantToProceedWithoutProofOfDeath,
)
from app.main.forms.exit_this_form import ExitThisForm
from app.main.forms.have_you_previously_made_a_request import (
    HaveYouPreviouslyMadeARequest,
)
from app.main.forms.choose_your_order_type import (
    ChooseYourOrderType,
)
from app.main.forms.how_we_process_requests import HowTheProcessWorks
from app.main.forms.is_service_person_alive import IsServicePersonAlive
from app.main.forms.service_branch import ServiceBranch
from app.main.forms.service_person_details import ServicePersonDetails
from app.main.forms.request_a_military_service_record import (
    RequestAMilitaryServiceRecord,
)
from app.main.forms.upload_a_proof_of_death import UploadAProofOfDeath
from app.main.forms.we_are_unlikely_to_hold_this_record import (
    WeAreUnlikelyToHoldThisRecord,
)
from app.main.forms.we_may_hold_this_record import WeMayHoldThisRecord
from app.main.forms.were_they_a_commissioned_officer import WereTheyACommissionedOfficer
from app.main.forms.what_was_their_date_of_birth import WhatWasTheirDateOfBirth
from app.main.forms.you_may_want_to_check_ancestry import YouMayWantToCheckAncestry
from app.main.forms.your_contact_details import YourContactDetails
from app.main.forms.what_is_your_address import WhatIsYourAddress
from flask import redirect, render_template, request, session, url_for


@bp.route("/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(RequestAMilitaryServiceRecord)
def start(form, state_machine):
    save_catalogue_reference_to_session(request)
    if form.validate_on_submit():
        state_machine.continue_from_start_form()
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/request_a_military_service_record.html", form=form, content=load_content()
    )


@bp.route("/how-we-process-requests/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(HowTheProcessWorks)
def how_we_process_requests(form, state_machine):
    if form.validate_on_submit():
        state_machine.continue_from_how_we_process_requests_form()
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/how-we-process-requests.html", form=form, content=load_content()
    )


@bp.route("/before-you-start/", methods=["GET", "POST"])
@with_state_machine
@with_route_for_back_link_saved_to_session(
    route=MultiPageFormRoutes.BEFORE_YOU_START.value
)
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
        "main/are-you-sure-you-want-to-cancel.html",
        form=form,
        content=load_content(),
        route_for_back_link=session.get("route_for_back_link", False),
    )


@bp.route("/you-have-cancelled-your-request/", methods=["GET"])
def you_have_cancelled_your_request():
    return render_template(
        "main/you-have-cancelled-your-request.html", content=load_content()
    )


@bp.route("/you-may-want-to-check-ancestry/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(YouMayWantToCheckAncestry)
def you_may_want_to_check_ancestry(form, state_machine):
    if form.validate_on_submit():
        state_machine.continue_from_you_may_want_to_check_ancestry_form()
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/you-may-want-to-check-ancestry.html",
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


@bp.route("/must-submit-subject-access/", methods=["GET", "POST"])
@with_state_machine
@with_route_for_back_link_saved_to_session(
    route=MultiPageFormRoutes.MUST_SUBMIT_SUBJECT_ACCESS_REQUEST.value
)
@with_form_prefilled_from_session(ExitThisForm)
def must_submit_subject_access_request(form, state_machine):
    if form.validate_on_submit():
        state_machine.continue_from_submit_subject_access_request_form(form)
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/must-submit-subject-access-request.html",
        form=form,
        content=load_content(),
        subject_access_request_link=ExternalLinks.SUBJECT_ACCESS_REQUEST_FORM,
    )


@bp.route("/only-living-subjects-can-request-their-record/", methods=["GET"])
def only_living_subjects_can_request_their_record():
    return render_template(
        "main/only-living-subjects-can-request-their-record.html",
        content=load_content(),
    )


@bp.route("/which-military-branch-did-the-person-serve-in/", methods=["GET", "POST"])
@with_form_prefilled_from_session(ServiceBranch)
@with_state_machine
def service_branch_form(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_service_branch_form(form)
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/which-military-branch-did-the-person-serve-in.html",
        form=form,
        content=load_content(),
    )


@bp.route("/were-they-a-commissioned-officer/", methods=["GET", "POST"])
@with_form_prefilled_from_session(WereTheyACommissionedOfficer)
@with_state_machine
def were_they_a_commissioned_officer(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_were_they_a_commissioned_officer_form(form)
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/were-they-a-commissioned-officer.html",
        form=form,
        content=load_content(),
    )


@bp.route("/we-do-not-have-royal-navy-service-branch-records/", methods=["GET", "POST"])
@with_form_prefilled_from_session(ExitThisForm)
@with_state_machine
@with_route_for_back_link_saved_to_session(
    route=MultiPageFormRoutes.WE_DO_NOT_HAVE_ROYAL_NAVY_SERVICE_RECORDS.value
)
def we_do_not_have_royal_navy_service_records(form, state_machine):
    if form.validate_on_submit():
        state_machine.continue_from_we_do_not_have_royal_navy_service_records_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/we-do-not-have-royal-navy-service-branch-records.html",
        form=form,
        content=load_content(),
        mod_service_link=ExternalLinks.MOD_SERVICE,
    )


@bp.route("/we-are-unlikely-to-hold-army-officer-records/", methods=["GET", "POST"])
@with_form_prefilled_from_session(WeAreUnlikelyToHoldThisRecord)
@with_route_for_back_link_saved_to_session(
    route=MultiPageFormRoutes.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__ARMY.value
)
@with_state_machine
def we_are_unlikely_to_hold_officer_records__army(form, state_machine):
    if form.validate_on_submit():
        state_machine.continue_from_we_are_unlikely_to_hold_officer_records_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/we-are-unlikely-to-hold-army-officer-records.html",
        content=load_content(),
        form=form,
        mod_service_link=ExternalLinks.MOD_SERVICE,
    )


@bp.route(
    "/we-are-unlikely-to-hold-royal-air-force-officer-records/", methods=["GET", "POST"]
)
@with_form_prefilled_from_session(WeAreUnlikelyToHoldThisRecord)
@with_route_for_back_link_saved_to_session(
    route=MultiPageFormRoutes.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__RAF.value
)
@with_state_machine
def we_are_unlikely_to_hold_officer_records__raf(form, state_machine):
    if form.validate_on_submit():
        state_machine.continue_from_we_are_unlikely_to_hold_officer_records_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/we-are-unlikely-to-hold-raf-officer-records.html",
        content=load_content(),
        form=form,
        mod_service_link=ExternalLinks.MOD_SERVICE,
        route_for_back_link=session.get("route_for_back_link", False),
    )


@bp.route(
    "/we-are-unlikely-to-hold-officer-records-for-this-branch/", methods=["GET", "POST"]
)
@with_route_for_back_link_saved_to_session(
    route=MultiPageFormRoutes.WE_ARE_UNLIKELY_TO_HOLD_OFFICER_RECORDS__GENERIC.value
)
@with_form_prefilled_from_session(WeAreUnlikelyToHoldThisRecord)
@with_state_machine
def we_are_unlikely_to_hold_officer_records__generic(form, state_machine):
    if form.validate_on_submit():
        state_machine.continue_from_we_are_unlikely_to_hold_officer_records_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/we-are-unlikely-to-hold-officer-records-for-this-branch.html",
        content=load_content(),
        form=form,
        mod_service_link=ExternalLinks.MOD_SERVICE,
        route_for_back_link=session.get("route_for_back_link", False),
    )


@bp.route("/we-are-unlikely-to-locate-this-record/", methods=["GET", "POST"])
@with_state_machine
@with_route_for_back_link_saved_to_session(
    route=MultiPageFormRoutes.WE_ARE_UNLIKELY_TO_LOCATE_THIS_RECORD.value
)
@with_form_prefilled_from_session(ExitThisForm)
def we_are_unlikely_to_locate_this_record(form, state_machine):
    if form.validate_on_submit():
        state_machine.continue_from_we_are_unlikely_to_locate_this_record_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/we-are-unlikely-to-locate-this-record.html",
        content=load_content(),
        form=form,
        paid_search_link=ExternalLinks.PAID_SEARCH,
    )


@bp.route("/we-may-hold-this-record/", methods=["GET", "POST"])
@with_form_prefilled_from_session(WeMayHoldThisRecord)
@with_route_for_back_link_saved_to_session(
    route=MultiPageFormRoutes.WE_MAY_HOLD_THIS_RECORD.value
)
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
        route_for_back_link=session.get("route_for_back_link", False),
    )


@bp.route(
    "/are-you-sure-you-want-to-proceed-without-proof-of-death/", methods=["GET", "POST"]
)
@with_form_prefilled_from_session(AreYouSureYouWantToProceedWithoutProofOfDeath)
@with_route_for_back_link_saved_to_session(
    route=MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_PROCEED_WITHOUT_PROOF_OF_DEATH.value
)
@with_state_machine
def are_you_sure_you_want_to_proceed_without_proof_of_death(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_are_you_sure_you_want_to_proceed_without_proof_of_death_form(
            form
        )
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/are-you-sure-you-want-to-proceed-without-proof-of-death.html",
        form=form,
        content=load_content(),
    )


@bp.route("/we-do-not-have-records-for-people-born-after/", methods=["GET", "POST"])
@with_route_for_back_link_saved_to_session(
    route=MultiPageFormRoutes.WE_DO_NOT_HAVE_RECORDS_FOR_PEOPLE_BORN_AFTER.value
)
@with_state_machine
@with_form_prefilled_from_session(ExitThisForm)
def we_do_not_have_records_for_people_born_after(form, state_machine):
    if form.validate_on_submit():
        state_machine.continue_from_we_do_not_have_records_for_people_born_after_form(
            form
        )
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/we-do-not-have-records-for-people-born-after.html",
        content=load_content(),
        form=form,
        mod_service_link=ExternalLinks.MOD_SERVICE,
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
        route_for_back_link=session.get("route_for_back_link", False),
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


@bp.route("/your-contact-details/", methods=["GET", "POST"])
@with_form_prefilled_from_session(YourContactDetails)
@with_state_machine
def your_contact_details(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_your_contact_details_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/your-contact-details.html", form=form, content=load_content()
    )


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


@bp.route("/what-is-your-address/", methods=["GET", "POST"])
@with_route_for_back_link_saved_to_session(
    route=MultiPageFormRoutes.WHAT_IS_YOUR_ADDRESS.value
)
@with_form_prefilled_from_session(WhatIsYourAddress)
@with_state_machine
def what_is_your_address(form, state_machine):
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_what_is_your_address_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/what-is-your-address.html",
        form=form,
        content=load_content(),
    )


@bp.route("/choose-your-order-type/", methods=["GET", "POST"])
@with_state_machine
def choose_your_order_type(state_machine):
    form = ChooseYourOrderType()
    if form.validate_on_submit():
        save_submitted_form_fields_to_session(form)
        state_machine.continue_from_choose_your_order_type_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/choose-your-order-type.html",
        form=form,
        content=load_content(),
    )


@bp.route("/upload-a-proof-of-death/", methods=["GET", "POST"])
@with_form_prefilled_from_session(UploadAProofOfDeath)
@with_state_machine
def upload_a_proof_of_death(form, state_machine):

    valid_submission = form.validate_on_submit()

    correct_back_link = get_back_link_route(
        current_route=MultiPageFormRoutes.UPLOAD_A_PROOF_OF_DEATH.value,
        valid_submission=valid_submission,
        back_link_in_session=session.get("route_for_back_link", False),
    )

    if correct_back_link:
        session["route_for_back_link"] = correct_back_link

    if valid_submission:
        state_machine.continue_from_upload_a_proof_of_death_form(form)
        return redirect(url_for(state_machine.route_for_current_state))
    return render_template(
        "main/upload-a-proof-of-death.html",
        form=form,
        content=load_content(),
        route_for_back_link=session.get("route_for_back_link", False),
    )


@bp.route("/your-order-summary/", methods=["GET"])
def your_order_summary():
    return render_template(
        "main/your-order-summary.html",
        content=load_content(),
        route_for_back_link=session.get("route_for_back_link", False),
    )


@bp.route("/request-submitted/", methods=["GET"])
def request_submitted():
    return render_template(
        "main/request-submitted.html",
        reference_number="123456",
        content=load_content(),
    )
