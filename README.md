# Request a service record

> [!TIP]
> This project was generated from the [TNA Flask Template](https://github.com/nationalarchives/flask-application-template), so you'll find the setup information in its README.

## Overview

New approaches used in this service are:

- the use of a state machine to determine a user's next step in the process
- the use of a single YAML file to hold all page and form content

## The state machine

This application uses the [Python StateMachine](https://pypi.org/project/python-statemachine/) library under the MIT licence to implement a state machine. The state machine comprises:

- **States** - representing a page or form in the service. Each state has data attached to it, such as the `_route_for_current_state`
- **Events** - representing a transition from one state to another, sometimes with conditions attached.

An example state would be `have_you_checked_the_catalogue_form`:

```python
have_you_checked_the_catalogue_form = State(enter="entering_have_you_checked_the_catalogue_form", final=True)
```

This is a final state, meaning that once the user reaches this state they cannot transition to any other state. The `enter` parameter specifies a method to be called when the state is entered.

An example event would be `continue_from_service_branch_form`

```python
continue_from_service_branch_form = (
        initial.to(was_service_person_officer_form, unless="go_to_mod or likely_unfindable")
        | initial.to(we_do_not_have_this_record_page, cond="go_to_mod")
        | initial.to(we_may_be_unable_to_find_this_record_page, cond="likely_unfindable")
)
```

Here we're saying that there are three possible transitions in response to this event, all of which correspond to what is returned by the conditions.
