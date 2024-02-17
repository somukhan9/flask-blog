from sqlalchemy import ForeignKey
from project import db

from project.g_models import BaseModel


class Category(BaseModel):
    __tablename__ = "category"

    title = db.Column(db.String(100), nullable=False)
    posts = db.relationship("Post", backref="category", lazy=True)

    def __repr__(self) -> str:
        return f"{self.title}"


class Post(BaseModel):
    __tablename__ = "post"

    title = db.Column(db.String(255), unique=True, nullable=False)
    slug = db.Column(db.String(300), unique=True, nullable=False)
    body = db.Column(db.Text(), nullable=False)
    summary = db.Column(db.String(255), nullable=True)
    featured_image = db.Column(db.Text(), nullable=True)
    user_id = db.Column(db.String(32), ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.String(32), ForeignKey(
        "category.id"), nullable=False)
    images = db.relationship("PostImage", backref="post",
                             cascade="all, delete", lazy=True)
    comments = db.relationship(
        "Comment", backref="post", cascade="all, delete", lazy=True)

    def __repr__(self) -> str:
        return f"{self.title}"


class PostImage(BaseModel):
    __tablename__ = "post_image"

    url = db.Column(db.Text(), nullable=False)
    post_id = db.Column(db.String(32), ForeignKey("post.id"), nullable=False)

    def __repr__(self) -> str:
        return super().__repr__()


class Comment(BaseModel):
    __tablename__ = "comment"

    content = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.String(32), ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.String(32), ForeignKey("post.id"), nullable=False)

    def __repr__(self) -> str:
        return f"{self.content}"
