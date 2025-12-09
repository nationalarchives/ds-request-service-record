import pytest
from app.constants import MultiPageFormRoutes
from app.lib.get_back_link_route import get_back_link_route


@pytest.mark.parametrize(
    "current_route, valid_submission, back_link_in_session, expected",
    [
        (
            MultiPageFormRoutes.UPLOAD_A_PROOF_OF_DEATH.value,
            True,
            "any",
            MultiPageFormRoutes.UPLOAD_A_PROOF_OF_DEATH.value,
        ),
        (
            MultiPageFormRoutes.UPLOAD_A_PROOF_OF_DEATH.value,
            False,
            "other_route",
            MultiPageFormRoutes.DO_YOU_HAVE_A_PROOF_OF_DEATH.value,
        ),
        (
            MultiPageFormRoutes.UPLOAD_A_PROOF_OF_DEATH.value,
            False,
            MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_PROCEED_WITHOUT_PROOF_OF_DEATH.value,
            MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_PROCEED_WITHOUT_PROOF_OF_DEATH.value,
        ),
        ("some_other_route", True, "any", None),
        (None, None, None, None),
    ],
)
def test_get_back_link_route(
    current_route, valid_submission, back_link_in_session, expected
):
    result = get_back_link_route(
        current_route=current_route,
        valid_submission=valid_submission,
        back_link_in_session=back_link_in_session,
    )
    assert result == expected
