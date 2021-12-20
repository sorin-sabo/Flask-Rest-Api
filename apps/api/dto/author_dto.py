"""
Author related data transfer object
"""

from flask_restx import Namespace, fields


class AuthorDto:
    """
    Author data transfer object definitions
    """

    api = Namespace('authors', description='Author related operations')

    author_basic = api.model('Author Basic', {
        'label': fields.String(readOnly=True, description='Author name', attribute='name'),
        'value': fields.Integer(readOnly=True, description='Author identifier', attribute='id'),
    })

    author = api.model('Author', {
        'id': fields.Integer(description='Author identifier'),
        'first_name': fields.String(description='Author first name', required=True),
        'last_name': fields.String(description='Author last name', required=True),
        'avatar': fields.String(description='Author avatar', required=True),
        'birthday': fields.Date(description='Author birthday', required=True),
        'user_id': fields.Integer(description='Author internal user identifier.', required=False)
    })
