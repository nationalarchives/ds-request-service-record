from app.lib.content import load_content
from app.lib.state_machine.state_machine_decorator import with_state_machine
from app.main import bp
from app.main.forms.start_now import StartNow
from app.main.forms.is_service_person_alive import IsServicePersonAlive
from app.main.forms.service_branch import ServiceBranch
from app.main.forms.have_you_checked_the_catalogue import HaveYouCheckedTheCatalogue
from flask import redirect, render_template, session, url_for


@bp.route("/start/", methods=["GET", "POST"])
@with_state_machine
def start(state_machine):
    form = StartNow()

    if form.validate_on_submit():
        state_machine.continue_to_have_you_checked_the_catalogue_form()
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/multi-page-journey/start.html", form=form, content=load_content()
    )

@bp.route("/have-you-checked-the-catalogue/", methods=["GET", "POST"])
@with_state_machine
def have_you_checked_the_catalogue(state_machine):
    form = HaveYouCheckedTheCatalogue()

    if form.validate_on_submit():
        pass
        # TODO: remove this line when successful submissions are handled in state machine

    return render_template(
        "main/multi-page-journey/have-you-checked-the-catalogue.html", form=form, content=load_content()
    )

@bp.route("/is-service-person-alive/", methods=["GET", "POST"])
@with_state_machine
def is_service_person_alive(state_machine):
    form = IsServicePersonAlive()

    if form.validate_on_submit():
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
@with_state_machine
def service_branch_form(state_machine):
    form = ServiceBranch()

    if form.validate_on_submit():
        state_machine.continue_from_service_branch_form(form)
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/multi-page-journey/service-branch.html", form=form, content=load_content()
    )


@bp.route("/mod-have-this-record/", methods=["GET"])
def mod_have_this_record():
    return render_template(
        "main/multi-page-journey/mod-have-this-record.html", content=load_content()
    )


@bp.route("/was-service-person-officer/", methods=["GET"])
def was_service_person_officer_form():
    return render_template(
        "main/multi-page-journey/was-service-person-an-officer.html", content=load_content()
    )


@bp.route("/check-ancestry/", methods=["GET"])
def check_ancestry():
    return render_template(
        "main/multi-page-journey/check-ancestry.html", content=load_content()
    )
