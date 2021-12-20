"""
Book related functions - services
"""


from apps.api.models import Book


def list_books():
    """
    List books
    """
    return Book.query.order_by(Book.title).all()
