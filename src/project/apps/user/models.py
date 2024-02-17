from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin


from project import db
from project.g_models import BaseModel


class User(BaseModel, UserMixin):
    __tablename__ = "user"

    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(355), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.Text(), nullable=True)
    posts = db.relationship("Post", backref="author",
                            cascade="all, delete", lazy=True)
    comments = db.relationship(
        "Comment", backref="author", cascade="all, delete", lazy=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return self.email
