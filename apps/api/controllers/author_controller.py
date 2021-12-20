"""
Author related endpoints
"""

from flask import request
from flask_restx import Resource

from apps.api.dto import AuthorDto
from apps.api.services import (
    list_authors,
    get_author,
    create_author,
)
from apps.api.utils import (
    response_with,
    responses as resp,
    requires_auth,
    get_current_user
)

api = AuthorDto.api
_author = AuthorDto.author
_author_basic = AuthorDto.author_basic


@api.route('/')
class AuthorsCollection(Resource):
    """
    Collection for root - / - endpoint

    Args:
        Resource (Object)

    Returns:
        json: data
    """

    @api.doc(
        'Author save',
        responses={
            200: ('author', _author),
            400: 'Invalid payload',
            401: 'Unauthorized'
        },
    )
    @requires_auth
    @api.expect(_author)
    def post(self):
        """
        Creates a new author.
        """

        user = get_current_user()
        payload = request.get_json()

        if payload is None or not isinstance(payload, dict):
            return response_with(resp.BAD_REQUEST_400)

        payload['user_id'] = user.id if user is not None else None
        author = get_author(user=user, fail_silently=True)
        result = create_author(payload, author)
        response = api.marshal(result, _author)

        return response_with(resp.SUCCESS_200, value={'data': response})

    @api.doc(
        'Author details',
        responses={
            200: ('author', _author),
            400: 'Invalid payload',
            401: 'Unauthorized',
            404: 'Not found'
        },
    )
    @requires_auth
    def get(self):
        """
        Returns author details
        """

        user = get_current_user()
        author = get_author(user)
        response = api.marshal(author, _author)

        return response_with(resp.SUCCESS_200, value={'data': response})


@api.route('/basic/list')
class AuthorsBasicCollection(Resource):
    """
    Collection for root - /basic/list - endpoint

    Args:
        Resource (Object)

    Returns:
        json: data
    """

    @api.doc(
        'Author basic list',
        responses={
            200: ('data', _author_basic),
            400: 'Invalid payload',
            401: 'Unauthorized',
            404: 'Not found'
        },
    )
    def get(self):
        """
        Returns author basic list
        """

        authors = list_authors()
        response = api.marshal(authors, _author_basic)

        return response_with(resp.SUCCESS_200, value={'data': response})
