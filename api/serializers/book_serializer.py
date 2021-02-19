from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from api.models import Book
from .author_serializer import AuthorBasicSerializer


class BookBasicSerializer(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Book
        fields = ('id', 'title')


class BookDetailSerializer(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Book


class BookListSerializer(ModelSchema):
    author = fields.Nested(AuthorBasicSerializer, only=['name'])

    class Meta(ModelSchema.Meta):
        model = Book
        fields = ('id', 'title', 'year', 'author')
