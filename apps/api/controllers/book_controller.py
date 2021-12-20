"""
Book related endpoints
"""

from flask_restx import Resource

from apps.api.dto import BookDto
from apps.api.services import (
    list_books,
)
from apps.api.utils import (
    response_with,
    responses as resp,
    requires_auth,
)

api = BookDto.api
_book = BookDto.book
_book_basic = BookDto.book_basic


@api.route('/basic/list')
class BooksBasicCollection(Resource):
    """
    Collection for root - /basic/list - endpoint

    Args:
        Resource (Object)

    Returns:
        json: data
    """

    @api.doc(
        'Book basic list',
        responses={
            200: ('data', _book),
        },
    )
    def get(self):
        """
        Returns book list
        """

        authors = list_books()
        response = api.marshal(authors, _book)

        return response_with(resp.SUCCESS_200, value={'data': response})


@api.route('/')
class BooksCollection(Resource):
    """
    Collection for root - / - endpoint

    Args:
        Resource (Object)

    Returns:
        json: data
    """

    @api.doc(
        'Book list',
        responses={
            200: ('data', _book_basic),
            401: 'Unauthorized'
        },
    )
    @requires_auth
    def get(self):
        """
        Returns book basic list
        """

        authors = list_books()
        response = api.marshal(authors, _book_basic)

        return response_with(resp.SUCCESS_200, value={'data': response})
