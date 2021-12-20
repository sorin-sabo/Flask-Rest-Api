"""
Author related model
"""

from apps.extensions import db
from .audit import BaseModel


books = db.Table(
    'author_book',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)


class Author(BaseModel):
    """
    Author database model.
    Used for storing author profile and personal details.
    """

    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    avatar = db.Column(db.String(255), nullable=True)
    books = db.relationship('Book', secondary=books, lazy='subquery',
                            backref=db.backref('authors', lazy=True))
    birthday = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @property
    def name(self):
        """
        Author full name
        """

        first_name = f'{self.first_name} ' if self.first_name is not None else ''
        last_name = self.last_name if self.last_name is not None else ''

        return f'{first_name}{last_name}'.strip()

    def __repr__(self):
        """
        Author representation
        """

        return self.name
