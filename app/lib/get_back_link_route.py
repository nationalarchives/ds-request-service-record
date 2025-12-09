from app.constants import MultiPageFormRoutes


def get_back_link_route(
    current_route=None, valid_submission=None, back_link_in_session=None
):
    """
    Determines the appropriate back link route for those pages where doing so is not
    straightforward.

    Args:
        current_route (str, optional): The current route where the function is being called. We use this to determine the logic to apply
        valid_submission (bool, optional): Indicates if the route is being called in response to a valid form submission
        back_link_in_session (str, optional): The back link route currently stored in the session

    Returns:
        str or None: The route to use for the back link, or `None` if no suitable route is found.
    """
    if current_route == MultiPageFormRoutes.UPLOAD_A_PROOF_OF_DEATH.value:
        if valid_submission:
            return MultiPageFormRoutes.UPLOAD_A_PROOF_OF_DEATH.value
        elif (
            back_link_in_session
            != MultiPageFormRoutes.ARE_YOU_SURE_YOU_WANT_TO_PROCEED_WITHOUT_PROOF_OF_DEATH.value
        ):
            return MultiPageFormRoutes.DO_YOU_HAVE_A_PROOF_OF_DEATH.value
        return back_link_in_session
    return None
