# encoding: utf-8
"""
Serialization schemas for Author resources REST API
----------------------------------------------------
"""

from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apps.api.models import Author, Book


class BookSchema(SQLAlchemyAutoSchema):
    """
    Base team schema exposes only the most general fields
    """

    label = fields.String(required=False, attribute='name')
    value = fields.Integer(required=True, attribute='id')

    class Meta:
        """
        Options for object schema
        """
        model = Book
        fields = ('label', 'value')
        transient = True
        load_instance = True
        include_relationships = True


class AuthorSchema(SQLAlchemyAutoSchema):
    """
    Author schema exposes only the most general fields
    """

    id = fields.Integer(required=False)
    first_name = fields.String(required=True, validate=[validate.Length(min=1, max=250)])
    last_name = fields.String(required=True, validate=[validate.Length(min=1, max=250)])
    books = fields.Nested(BookSchema, many=True, required=True)
    birthday = fields.String(required=True, validate=[validate.Length(min=1, max=250)])
    user_id = fields.Integer(required=True)

    class Meta:
        """
        Options defined for Schema
        """

        model = Author
        load_instance = True
        include_relationships = True
        fields = (
            'id', 'first_name', 'last_name', 'books', 'birthday', 'user_id'
        )
