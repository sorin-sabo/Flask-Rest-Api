"""
User related model
"""

import enum
from apps.extensions import db
from .audit import BaseModel


class UserType(enum.Enum):
    """
    User types enum definition
    """

    AUTHOR = "AUTHOR"
    READER = "READER"


class User(BaseModel):
    """
    User database model
    """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    user_type = db.Column(db.Enum(UserType), default='AUTHOR')

    @classmethod
    def find_by_email(cls, email):
        """
        Find user by email
        """
        return cls.query.filter_by(email=email).first()
