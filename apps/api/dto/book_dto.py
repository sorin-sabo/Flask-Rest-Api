"""
Book related data transfer object
"""

from flask_restx import Namespace, fields


class BookDto:
    """
    Book data transfer object definitions
    """

    api = Namespace('books', description='Book related operations')

    book_basic = api.model('Book Basic', {
        'label': fields.String(readOnly=True, description='Book title', attribute='title'),
        'value': fields.Integer(readOnly=True, description='Book identifier', attribute='id'),
    })

    book = api.model('Book', {
        'id': fields.Integer(description='Author identifier'),
        'title': fields.String(description='Book title', required=True),
        'year': fields.Integer(description='Book year', required=True),
        'author': fields.String(description='Book author.', required=False)
    })
