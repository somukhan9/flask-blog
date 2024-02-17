from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

from project.apps.blog.models import Post


def is_owner(f):
    @wraps(f)
    def decorated_function(slug, *args, **kwargs):
        post = Post.query.filter_by(slug=slug).first_or_404()
        if current_user.id != post.user_id:
            flash("This operation is forbidden for you!", "danger")
            return redirect(url_for("blog.home"))
        return f(slug, *args, **kwargs)
    # print("-------yellow---------")
    return decorated_function
