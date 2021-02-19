from api.utils import db


class BaseModel(db.Model):
    """
    Abstract data model to be extended in all models.
    """

    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
