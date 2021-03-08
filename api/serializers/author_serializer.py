from marshmallow import fields, validate
from marshmallow_sqlalchemy import ModelSchema
from flask_restx import fields as x_fields

from api.models import Author
from api.app import api


class AuthorBasicSerializer(ModelSchema):
    name = fields.Method(serialize="_get_name")

    class Meta(ModelSchema.Meta):
        model = Author
        fields = ('id', 'name')

    @staticmethod
    def _get_name(author):
        return author.__repr__()


class AuthorDetailSerializer(ModelSchema):
    first_name = fields.Str(required=True, validate=[validate.Length(min=4, max=250)])
    last_name = fields.Str(required=True, validate=[validate.Length(min=4, max=250)])
    avatar = fields.Str(required=False, validate=[validate.Length(min=4, max=250)])

    class Meta(ModelSchema.Meta):
        model = Author
        fields = ('id', 'first_name', 'last_name', 'avatar', 'created_by', 'updated_by')


class AuthorListSerializer(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Author
        fields = ('id', 'first_name', 'last_name', 'avatar')


author_detail = api.model('Author', {
    'id': x_fields.Integer(readOnly=True, description='The unique identifier of an author'),
    'first_name': x_fields.String(required=True, description='Author first name'),
    'last_name': x_fields.String(required=True, description='Author last name'),
    'avatar': x_fields.String(required=True, description='Author avatar image'),
})
