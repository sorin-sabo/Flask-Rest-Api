from flask import request, Blueprint
from flask_jwt_extended import jwt_required

from api.models import Author
from api.serializers import AuthorListSerializer, AuthorDetailSerializer, AuthorBasicSerializer
from api.utils import db, ValidationException, response_with, responses as resp

author_routes = Blueprint("author_routes", __name__)


@author_routes.route('/', methods=['POST'])
def create_author():
    try:
        data = request.get_json()
        author_schema = AuthorDetailSerializer()
        author = author_schema.load(data)
        result = author_schema.dump(author.create())

        return response_with(resp.SUCCESS_201, value={"author": result})
    except ValidationException:
        return response_with(resp.BAD_REQUEST_400)


@author_routes.route('/basic/list', methods=['GET'])
def get_author_basic_list():
    fetched = Author.query.all()
    author_schema = AuthorBasicSerializer(many=True)
    authors = author_schema.dump(fetched)

    return response_with(resp.SUCCESS_200, value={"authors": authors})


@author_routes.route('/', methods=['GET'])
def get_author_list():
    fetched = Author.query.all()
    author_schema = AuthorListSerializer(many=True)
    authors = author_schema.dump(fetched)

    return response_with(resp.SUCCESS_200, value={"authors": authors})


@author_routes.route('/<int:author_id>', methods=['GET'])
def get_author_detail(author_id):
    fetched = Author.query.get_or_404(author_id)
    author_schema = AuthorDetailSerializer()
    author = author_schema.dump(fetched)

    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:author_id>', methods=['PUT'])
@jwt_required
def update_author_detail(author_id):
    data = request.get_json()
    get_author = Author.query.get_or_404(author_id)
    get_author.first_name = data['first_name']
    get_author.last_name = data['last_name']
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorDetailSerializer()
    author = author_schema.dump(get_author)

    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:author_id>', methods=['PATCH'])
def modify_author_detail(author_id):
    data = request.get_json()
    get_author = Author.query.get(author_id)

    if data.get('first_name'):
        get_author.first_name = data['first_name']

    if data.get('last_name'):
        get_author.last_name = data['last_name']

    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorDetailSerializer()
    author = author_schema.dump(get_author)

    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()

    return response_with(resp.SUCCESS_204)
