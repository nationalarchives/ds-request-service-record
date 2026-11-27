import pytest

from app import create_app


@pytest.fixture
def officer_client():
    # Disable CSRF so these tests focus on the submitted branch rather than the token.
    app = create_app("config.Test")
    app.config["WTF_CSRF_ENABLED"] = False
    client = app.test_client()
    prefix = app.config["SERVICE_URL_PREFIX"]

    # Enter the journey and keep an existing answer to check it is not overwritten.
    client.get(f"{prefix}/")
    with client.session_transaction(path=f"{prefix}/") as session:
        session["form_data"] = {"service_branch": "BRITISH_ARMY"}
    return client, prefix


# Test a missing hidden field separately from an empty or unrecognised value.
@pytest.mark.parametrize(
    "branch_data",
    [
        pytest.param({}, id="missing"),
        pytest.param({"service_branch": ""}, id="empty"),
        pytest.param({"service_branch": "INVALID"}, id="unrecognised"),
    ],
)
# Every valid officer answer should trigger the same recovery for an invalid branch.
@pytest.mark.parametrize("officer", ["yes", "no", "unknown"])
def test_invalid_branch_redirects_without_saving(
    officer_client, branch_data, officer, caplog
):
    client, prefix = officer_client

    # Submit the officer answer with the chosen invalid hidden-field data.
    response = client.post(
        f"{prefix}/were-they-a-commissioned-officer/",
        data={**branch_data, "were_they_a_commissioned_officer": officer},
    )

    # The user is sent back to branch selection, not onward in the journey.
    assert response.status_code == 302
    assert (
        response.location == f"{prefix}/which-military-branch-did-the-person-serve-in/"
    )

    # pytest's caplog fixture captures log records so we can check the warning
    # describes the recovery without including submitted values.
    assert any(
        record.levelname == "WARNING"
        and record.getMessage()
        == (
            "Commissioned officer submission has a missing or invalid service branch; "
            "redirecting to branch selection."
        )
        for record in caplog.records
    )

    # Neither the invalid branch nor the officer answer is saved to the session.
    with client.session_transaction(path=f"{prefix}/") as session:
        assert session["form_data"] == {"service_branch": "BRITISH_ARMY"}
