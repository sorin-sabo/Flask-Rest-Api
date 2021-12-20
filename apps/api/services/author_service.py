"""
Author related functions - services
"""

from marshmallow.exceptions import ValidationError
from apps.extensions import db
from apps.api.models import Author, Book
from apps.api.schemas import AuthorSchema
from apps.api.utils import NotFound


def list_authors():
    """
    List authors
    """
    return Author.query.order_by(Author.first_name, Author.last_name).all()


def get_author(user=None, fail_silently=False):
    """
    Get author by request user

    :param User user: Request user
    :param bool fail_silently: Indicates if exception should be raised
                               in case author is not found. In case is
                               set to True and author not found - exception
                               is not raised, return None. In case is set
                               to False and author not found - exception is raised.
                               Defaults to False.
    :return Found author by request user
    :rtype Author, NoneType
    :raises NotFound exception in case author not found for current user
    """

    if user is None:
        raise NotFound('Author not found')

    author = Author.query.filter_by(user_id=user.id).first()

    if author is None and not fail_silently:
        raise NotFound('Author not found')

    return author


def create_author(payload=None, author=None):
    """
    Create/Update author using payload data
    Request user can be associated only with one author.
    Create new author in case request user is associated with no author otherwise update it.

    :param dict payload: Request data payload
    :param Author author: Found author using request user
    """

    if payload is None:
        raise ValidationError("Invalid payload")

    # Validate payload
    author_schema = AuthorSchema()
    author_schema.load(payload, transient=True)

    books = payload.pop("books")

    if author is not None:
        author.first_name = payload.get('first_name', author.first_name)
        author.last_name = payload.get('last_name', author.last_name)
        author.birthday = payload.get('birthday', author.birthday)
    else:
        author = Author(**payload)

    # Update genres
    book_ids = [book['value'] for book in books]
    books = Book.query.filter(Book.id.in_(book_ids)).all()
    author.books = books

    # Save author
    db.session.add(author)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return author
