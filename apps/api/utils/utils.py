"""
Utility methods definition
"""

# noinspection PyProtectedMember
from flask import _request_ctx_stack, has_request_context, g


def get_current_user():
    """
    A proxy for the current user. If no user is logged in, this will be an empty user.

    :return Request context user or None.
    """
    current_user = None

    if has_request_context() and hasattr(_request_ctx_stack.top, 'user'):
        current_user = _request_ctx_stack.top.user

    # global user is set only for unit tests
    elif hasattr(g, 'user'):
        current_user = g.user

    return current_user
