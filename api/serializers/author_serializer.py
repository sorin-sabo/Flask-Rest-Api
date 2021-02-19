from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from api.models import Author


class AuthorBasicSerializer(ModelSchema):
    name = fields.Method(serialize="_get_name")

    class Meta(ModelSchema.Meta):
        model = Author
        fields = ('id', 'name')

    @staticmethod
    def _get_name(author):
        return author.__repr__()


class AuthorDetailSerializer(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Author


class AuthorListSerializer(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Author
        fields = ('id', 'first_name', 'last_name', 'avatar')
