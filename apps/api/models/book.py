"""
Book related model
"""

from apps.extensions import db
from .audit import BaseModel


class Book(BaseModel):
    """
    Book database model.
    Used for storing authors books details.
    """

    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    year = db.Column(db.Integer)

    def __repr__(self):
        """
        Book representation
        """
        return f"<Book {self.title}>"
