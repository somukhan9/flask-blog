from datetime import datetime
from uuid import uuid4

from project import db


def get_uuid():
    return uuid4().hex


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(32), primary_key=True, unique=True,
                   nullable=False, default=get_uuid)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
