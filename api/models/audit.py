from sqlalchemy.ext.declarative import declared_attr

from api.utils import db


class BaseModel(db.Model):
    """
    Abstract data model to be extended in all models.
    """

    __abstract__ = True

    @declared_attr
    def created_by(self):
        return db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    @declared_attr
    def updated_by(self):
        return db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
