from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin


from project import db
from project.g_models import BaseModel

default_profile_image = "https://media.istockphoto.com/id/1930140152/photo/white-neutral-head-of-a-mannequin-figure-in-minimalist-style-on-a-metal-stand-against-a-light.jpg?s=1024x1024&w=is&k=20&c=auXdY9zujtOkGWGLwLKlYAadd_VChQ69-Wn1uoeUE0A="


class User(BaseModel, UserMixin):
    __tablename__ = "user"

    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(355), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.Text(), default=default_profile_image)
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
