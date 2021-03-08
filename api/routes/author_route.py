from flask import request
from flask_restx import Resource

from api.models import Author
from api.app import api
from api.serializers import (
    AuthorListSerializer,
    AuthorDetailSerializer,
    AuthorBasicSerializer,
    author_detail
)
from api.utils import (
    response_with,
    responses as resp,
    requires_auth,
    get_current_user,
    db
)

author_ns = api.namespace('authors', description='Operations related to authors.')


@author_ns.route('/')
class AuthorsCollection(Resource):
    @requires_auth
    @api.expect(author_detail)
    def post(self):
        """
        Creates a new author.
        """

        data = request.get_json()
        user = get_current_user()
        user_id = user.id if user is not None else None
        author_schema = AuthorDetailSerializer()
        data.update(dict(created_by=user_id, updated_by=user_id))
        author = author_schema.load(data, transient=True)
        result = author_schema.dump(author.create())

        return response_with(resp.SUCCESS_201, value={"author": result})

    @requires_auth
    def get(self):
        """
        Returns list of authors.
        """

        fetched = Author.query.all()
        author_schema = AuthorListSerializer(many=True)
        authors = author_schema.dump(fetched)

        return response_with(resp.SUCCESS_200, value={"authors": authors})


@author_ns.route('/basic')
class AuthorsBasicCollection(Resource):
    @requires_auth
    def get(self):
        """
        Returns basic list of authors.
        """

        fetched = Author.query.all()
        author_schema = AuthorBasicSerializer(many=True)
        authors = author_schema.dump(fetched)

        return response_with(resp.SUCCESS_200, value={"authors": authors})


# noinspection PyUnresolvedReferences
@author_ns.route('/<int:author_id>')
class AuthorDetail(Resource):
    @requires_auth
    @api.response(404, 'Author not found.')
    def get(self, author_id):
        """
        Returns an author.
        """

        fetched = Author.query.get_or_404(author_id)
        author_schema = AuthorDetailSerializer()
        author = author_schema.dump(fetched)

        return response_with(resp.SUCCESS_200, value={"author": author})

    @requires_auth
    @api.response(404, 'Author not found.')
    def put(self, author_id):
        """
        Updates an author.

        Use this method to change the first name ans last name of an author.

        * Send a JSON object with the new first_name and last_name in the request body.

        ```
        {
          "first_name": "New Author First Name",
          "last_name": "New Author Last Name"
        }
        ```

        * Specify the ID of the author to modify in the request URL path.
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

    @requires_auth
    @api.response(204, 'Author successfully deleted.')
    def delete(self, author_id):
        """
        Deletes an author.
        """

        author = Author.query.get_or_404(author_id)
        db.session.delete(author)
        db.session.commit()

        return response_with(resp.SUCCESS_204)
