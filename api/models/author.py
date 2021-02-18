from api.utils import db
from .audit import BaseModel


class Author (BaseModel):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    avatar = db.Column(db.String(255), nullable=True)
    books = db.relationship('Book', backref='Author', cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, books=None):
        self.first_name = first_name
        self.last_name = last_name
        self.books = books

    def __repr__(self):
        first_name = f'{self.first_name} ' if self.first_name is not None else ''
        last_name = self.last_name if self.last_name is not None else ''

        return f'{first_name}{last_name}'.strip()
