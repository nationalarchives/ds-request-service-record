from app.lib.content import load_content
from app.lib.decorators.state_machine_decorator import with_state_machine
from app.lib.decorators.with_form_prefilled_from_session import with_form_prefilled_from_session
from app.main import bp
from app.main.forms.start_now import StartNow
from app.main.forms.is_service_person_alive import IsServicePersonAlive
from app.main.forms.service_branch import ServiceBranch
from app.main.forms.have_you_checked_the_catalogue import HaveYouCheckedTheCatalogue
from app.main.forms.was_service_person_an_officer import WasServicePersonAnOfficer
from flask import redirect, render_template, session, url_for


@bp.route("/start/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(StartNow)
def start(form, state_machine):

    if form.validate_on_submit():
        state_machine.continue_to_have_you_checked_the_catalogue_form()
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/multi-page-journey/start.html", form=form, content=load_content()
    )

@bp.route("/have-you-checked-the-catalogue/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(HaveYouCheckedTheCatalogue)
def have_you_checked_the_catalogue(form, state_machine):

    if form.validate_on_submit():
        session["have_you_checked_the_catalogue"] = form.have_you_checked_the_catalogue.data
        state_machine.continue_from_have_you_checked_the_catalogue_form(form)
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/multi-page-journey/have-you-checked-the-catalogue.html", form=form, content=load_content()
    )

@bp.route("/is-service-person-alive/", methods=["GET", "POST"])
@with_state_machine
@with_form_prefilled_from_session(IsServicePersonAlive)
def is_service_person_alive(form, state_machine):

    if form.validate_on_submit():
        session["is_service_person_alive"] = form.is_service_person_alive.data
        state_machine.continue_from_service_person_alive_form(form)
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/multi-page-journey/is-service-person-alive.html", form=form, content=load_content()
    )


@bp.route("/must-submit-subject-access/", methods=["GET"])
def must_submit_subject_access_request():
    return render_template(
        "main/multi-page-journey/must-submit-subject-access-request.html", content=load_content()
    )


@bp.route("/only-living-subjects-can-request-their-record/", methods=["GET"])
def only_living_subjects_can_request_their_record():
    return render_template(
        "main/multi-page-journey/only-living-subjects-can-request-their-record.html",
        content=load_content(),
    )


@bp.route("/service-branch/", methods=["GET", "POST"])
@with_form_prefilled_from_session(ServiceBranch)
@with_state_machine
def service_branch_form(form, state_machine):

    if form.validate_on_submit():
        session["service_branch"] = form.service_branch.data
        state_machine.continue_from_service_branch_form(form)
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/multi-page-journey/service-branch.html", form=form, content=load_content()
    )


@bp.route("/was-service-person-officer/", methods=["GET", "POST"])
@with_form_prefilled_from_session(WasServicePersonAnOfficer)
@with_state_machine
def was_service_person_an_officer(form, state_machine):
    if form.validate_on_submit():
        session["was_service_person_an_officer"] = form.was_service_person_an_officer.data
        state_machine.continue_from_was_service_person_officer_form(form)
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/multi-page-journey/was-service-person-an-officer.html", form=form, content=load_content()
    )


@bp.route("/search-the-catalogue/", methods=["GET"])
def search_the_catalogue():
    return render_template(
        "main/multi-page-journey/search-the-catalogue.html", content=load_content()
    )

@bp.route("/we-do-not-have-this-record/", methods=["GET"])
def we_do_not_have_this_record():
    return render_template(
        "main/multi-page-journey/we-do-not-have-this-record.html", content=load_content()
    )


@bp.route("/we-may-be-unable-to-find-this-record/", methods=["GET"])
def we_may_be_unable_to_find_this_record():
    return render_template(
        "main/multi-page-journey/we-may-be-unable-to-find-this-record.html", content=load_content()
    )

@bp.route("/we-may-hold-this-record/", methods=["GET", "POST"])
def we_may_hold_this_record():
    return render_template(
        "main/multi-page-journey/we-may-hold-this-record.html", content=load_content()
    )