from slugify import slugify

from flask import Blueprint, flash, redirect, render_template, request, url_for, g
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from project import db
from project.utils.cloudinary import upload_image, delete_image

from project.apps.blog.decorators import is_owner

from project.apps.blog.forms import AddCommentForm, PostForm
from project.apps.blog.models import Category, Comment, Post

from project.utils.cloudinary import upload_image

blog_blueprint = Blueprint(
    "blog",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# Global variables
@blog_blueprint.before_request
def get_all_categories():
    categories = Category.query.all()
    g.categories = categories


@blog_blueprint.route("/", methods=["GET"])
def home():
    latest_posts = Post.query.order_by(
        Post.created_at.desc()).limit(3).all()

    return render_template("blog/home.html", latest_posts=latest_posts)


@blog_blueprint.route("/search", methods=["GET"])
def search():
    q = request.args.get("q", "")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 6, type=int)
    if q:
        posts = Post.query.filter(or_(Post.title.ilike(f'%{q}%'), Post.body.ilike(f'%{q}%'))).paginate(
            page=page, per_page=per_page, error_out=False)
    else:
        posts = []

    return render_template("blog/search.html", posts=posts)


@blog_blueprint.route("/posts", methods=["GET"])
def posts():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 6, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    return render_template("blog/posts.html", posts=posts)


@blog_blueprint.route("/categories/<category_slug>", methods=["GET"])
def category_posts(category_slug):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 6, type=int)

    category = Category.query.filter_by(slug=category_slug).first_or_404()

    posts = Post.query.filter_by(category_id=category.id).order_by(
        Post.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return render_template("blog/category_posts.html", category=category, posts=posts)


@blog_blueprint.route("/posts/<slug>", methods=["GET", "POST"])
def single_post(slug):
    # print(request.url.split("/"))
    post = Post.query.filter_by(slug=slug).first_or_404()

    form = AddCommentForm()

    if request.method == "POST" and form.validate_on_submit():

        content = form.content.data
        comment = Comment(
            content=content, user_id=current_user.id, post_id=post.id)

        try:
            db.session.add(comment)
            db.session.commit()
        except Exception as ex:
            print(str(ex))
            flash("Something went wrong while commenting!", "danger")

    return render_template("blog/single_post.html", post=post, form=form)


@blog_blueprint.route("/create-blog", methods=["GET", "POST"])
@login_required
def create():
    form = PostForm()

    if form.validate_on_submit():
        try:
            featured_image = request.files.get("featured_image")
            data = upload_image(featured_image, "flask-blog/blog")

            new_post = Post(
                title=form.title.data,
                slug=slugify(form.title.data),
                body=form.body.data,
                summary=form.summary.data,
                # Handle file upload appropriately
                featured_image=data["secure_url"],
                user_id=current_user.id,
                category_id=form.category.data.id,
            )

            db.session.add(new_post)
            db.session.commit()

            flash(f"New Blog Post has been created successfully!", "success")
            return redirect(url_for('blog.home'))

        except IntegrityError as ex:
            violated_field = str(ex.orig).split(".")[1].split(" ")[0]
            print(violated_field)
            # print(str(ex.orig).split(".")[1])
            db.session.rollback()
            if violated_field == "title":
                flash(
                    f"This title has been taken by someone! Please try with another one.", "danger")

    return render_template("blog/create.html", form=form)


@blog_blueprint.route("/update-blog/<slug>", methods=["GET", "POST"])
@login_required
@is_owner
def update(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    categories = list(Category.query.all())

    if request.method == "POST":
        try:
            data = dict()
            featured_image = request.files.get("featured_image")
            if featured_image:
                # For image update I will delete the previous picture from the cloud and then upload the new one
                filename = post.featured_image.split("/")[-1]
                delete_image(filename, "flask-blog/blog")
                data = upload_image(featured_image, "flask-blog/blog")

            # If any field is empty then set the previous value as default
            post.title = request.form.get("title", post.title)
            post.slug = slugify(post.title)
            post.body = request.form.get("body", post.body)
            post.summary = request.form.get("summary", post.summary)
            post.category_id = request.form.get("category", post.category_id)
            post.featured_image = data.get("secure_url", post.featured_image)

            db.session.commit()

            flash(f"New Blog Post has been updated successfully!", "success")

            return redirect(url_for('blog.single_post', slug=post.slug))

        except IntegrityError as ex:
            violated_field = str(ex.orig).split(".")[1].split(" ")[0]
            print(violated_field)
            # print(str(ex.orig).split(".")[1])
            db.session.rollback()
            if violated_field == "title":
                flash(
                    f"This title has been taken by someone! Please try with another one.", "danger")

            else:
                flash(f"{str(ex.orig)}", "danger")
            print(str(ex.orig))

    return render_template("blog/update.html", post=post, categories=categories)


@blog_blueprint.route("/delete-blog/<slug>", methods=["POST"])
@login_required
@is_owner
def delete(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()

    try:
        # For image update I will delete the previous picture from the cloud and then upload the new one
        filename = post.featured_image.split("/")[-1]
        delete_image(filename, "flask-blog/blog")
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully!", "success")
        return redirect(url_for("blog.posts"))
    except Exception as ex:
        print(ex)
        flash("Failed to delete post!", "danger")

    return render_template("blog/single_post.html", post=post)


# Test function for testing image upload
# @blog_blueprint.route("/", methods=["POST"])
# def upload():
#     file = request.files.get("file")
#     # print(f"File ------> {file}")
#     data = upload_image(file, "flask-blog/user")
#     print(f"Data -------> {data}")
#     return redirect(url_for("blog.home"))


# # Test function for testing image destroy
# @blog_blueprint.route("/<filename>", methods=["GET"])
# def destroy(filename):
#     # print(f"File ------> {file}")
#     print("-------------hello get-----------------")
#     print(filename)
#     data = delete_image(
#         filename, "flask-blog/user")
#     print(f"Data -------> {data}")
#     return redirect(url_for("blog.home"))


# @blog_blueprint.route("/posts/<slug>/comment", methods=["GET", "POST"])
# def add_comment_to_post(slug):
#     form = AddCommentForm()
#     post = Post.query.filter_by(slug=slug).first_or_404()

#     if request.method == "POST":
#         content = form.content.data

#         if form.validate_on_submit():
#             comment = Comment(
#                 content=content, user_id=current_user.id, post_id=post.id)

#             try:
#                 db.session.add(comment)
#                 db.session.commit()
#             except Exception as ex:
#                 print(str(ex))
#                 flash("Something went wrong while commenting!", "danger")

#     return redirect(url_for("blog.single_post", slug=post.slug))
