from app.lib.content import load_content
from app.lib.state_machine.state_machine_decorator import with_state_machine
from app.main import bp
from app.main.forms.start_now import StartNow
from app.main.forms.is_service_person_alive import IsServicePersonAlive
from app.main.forms.service_branch import ServiceBranch
from flask import redirect, render_template, session, url_for


@bp.route("/start/", methods=["GET", "POST"])
@with_state_machine
def start(state_machine):
    form = StartNow()

    if form.validate_on_submit():
        state_machine.continue_to_service_person_alive_form()
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/multi-page-journey/start.html", form=form, content=load_content()
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


@bp.route("/service-branch/", methods=["GET"])
def service_branch_form():
    form = ServiceBranch()
    return render_template(
        "main/multi-page-journey/service-branch.html", form=form, content=load_content()
    )
