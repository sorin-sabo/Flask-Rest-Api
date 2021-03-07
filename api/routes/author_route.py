from flask import request, Blueprint

from api.models import Author
from api.serializers import (
    AuthorListSerializer,
    AuthorDetailSerializer,
    AuthorBasicSerializer,
)
from api.utils import (
    db,
    ValidationException,
    response_with,
    responses as resp,
    requires_auth,
    get_current_user
)

author_routes = Blueprint("author_routes", __name__)


@author_routes.route('/', methods=['POST'])
@requires_auth
def create_author():
    """
    Creates a new author.
    """
    try:
        data = request.get_json()
        user = get_current_user()
        user_id = user.id if user is not None else None
        author_schema = AuthorDetailSerializer()
        data.update(dict(created_by=user_id, updated_by=user_id))
        author = author_schema.load(data, transient=True)
        result = author_schema.dump(author.create())

        return response_with(resp.SUCCESS_201, value={"author": result})
    except ValidationException:
        return response_with(resp.BAD_REQUEST_400)


@author_routes.route('/basic/list', methods=['GET'])
@requires_auth
def get_author_basic_list():
    fetched = Author.query.all()
    author_schema = AuthorBasicSerializer(many=True)
    authors = author_schema.dump(fetched)

    return response_with(resp.SUCCESS_200, value={"authors": authors})


@author_routes.route('/', methods=['GET'])
@requires_auth
def get_author_list():
    fetched = Author.query.all()
    author_schema = AuthorListSerializer(many=True)
    authors = author_schema.dump(fetched)

    return response_with(resp.SUCCESS_200, value={"authors": authors})


@author_routes.route('/<int:author_id>', methods=['GET'])
@requires_auth
def get_author_detail(author_id):
    fetched = Author.query.get_or_404(author_id)
    author_schema = AuthorDetailSerializer()
    author = author_schema.dump(fetched)

    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:author_id>', methods=['PUT'])
@requires_auth
def update_author_detail(author_id):
    """
    Update author by id
    """

    data = request.get_json()
    existing_author = Author.query.get_or_404(author_id)

    author_schema = AuthorDetailSerializer()
    author_schema.load(data, transient=True)

    existing_author.first_name = data['first_name']
    existing_author.last_name = data['last_name']
    db.session.add(existing_author)
    db.session.commit()
    author = author_schema.dump(existing_author)

    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:author_id>', methods=['DELETE'])
@requires_auth
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()

    return response_with(resp.SUCCESS_204)
