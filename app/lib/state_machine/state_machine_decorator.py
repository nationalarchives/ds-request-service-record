from functools import wraps
import inspect
from flask import g
from app.lib.state_machine.state_machine import RoutingStateMachine


def with_state_machine(fn):
    """
    Decorator that provides a per-request RoutingStateMachine.

    Behavior:
    - Creates a new RoutingStateMachine instance for each request.
    - Stores the instance on Flask's per-request global `g`.
    - If the wrapped view function declares a `state_machine` parameter,
      injects the created instance into the call via keyword arguments.

    Notes:
    - Using `g` makes the instance accessible anywhere within the same request.
    - If all decorated views accept `state_machine`, the `inspect` check can be
      removed and the parameter can be unconditionally injected.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        sm = RoutingStateMachine()

        # Store the state machine on Flask's request-scoped `g` so other
        # code in the same request can access it without passing it around explicitly.
        g.state_machine = sm

        try:
            # Only inject the argument when the wrapped function explicitly
            # accepts a `state_machine` parameter. This keeps the decorator
            # compatible with views that do not expect it.
            if "state_machine" in inspect.signature(fn).parameters:
                kwargs["state_machine"] = sm
        except (ValueError, TypeError):
            # Some callables (e.g., builtins) may not expose
            # a retrievable signature; fail silently and avoid injection.
            pass

        # Call the original function with possibly augmented kwargs.
        return fn(*args, **kwargs)

    return wrapper
