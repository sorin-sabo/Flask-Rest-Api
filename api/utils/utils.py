# noinspection PyProtectedMember
from flask import _request_ctx_stack, has_request_context


def get_current_user():
    """
    A proxy for the current user. If no user is logged in, this will be an empty user.

    :return Request context user or None.
    """

    current_user = None

    if has_request_context() and hasattr(_request_ctx_stack.top, 'user'):
        current_user = _request_ctx_stack.top.user

    return current_user
