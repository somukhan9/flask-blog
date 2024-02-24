from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from sqlalchemy.exc import IntegrityError

from project.apps.blog.models import Post
from project.utils.cloudinary import delete_image, upload_image

from project.apps.user.forms import SignUpForm, LoginForm, UserUpdateForm


from project import db
from project.apps.user.models import User

user_blueprint = Blueprint(
    "user",
    __name__,
    template_folder="templates",
    static_folder="static"
)


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    # If the user is already authenticated then he/she should be redirected to home page
    if current_user.is_authenticated:
        return redirect(url_for("blog.home"))

    form = LoginForm(request.form)
    if request.method == "POST":
        email = form.data.get("email")
        password = form.data.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user=user)
            flash("Login Successful!", "success")
            return redirect(url_for("blog.home"))

        else:
            flash("Invalid credentials!", "danger")

    return render_template("user/login.html", form=form)


@user_blueprint.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    # If the user is already authenticated then he/she should be redirected to home page
    if current_user.is_authenticated:
        return redirect(url_for("blog.home"))

    form = SignUpForm()

    if request.method == "POST" and form.validate_on_submit():
        name = form.data.get("name")
        email = form.data.get("email")
        password = form.data.get("password")
        print(name, email, password)
        user = User(name=name, email=email)
        user.set_password(password=password)
        try:
            db.session.add(user)
            db.session.commit()
            print(user)
            flash('Registration Successful!', 'success')
            return redirect(url_for("user.login"))
        except IntegrityError as ex:
            violated_field = str(ex.orig).split(".")[1].split(" ")[0]
            print(violated_field)
            # print(str(ex.orig).split(".")[1])
            db.session.rollback()
            if violated_field == "email":
                flash(f"User with this email already exists!", "danger")
        except Exception as ex:
            print(str(ex._message))
            db.session.rollback()

    return render_template("user/sign-up.html", form=form)


@user_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))


@user_blueprint.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UserUpdateForm()
    user = User.query.get_or_404(current_user.id)

    if request.method == "POST":
        try:
            name = form.name.data or current_user.name
            email = form.email.data or current_user.email
            profile_image = request.files.get("profile_image", None)

            data = None

            if profile_image:
                # For image update I will delete the previous picture from the cloud and then upload the new one
                filename = None
                if user.profile_image:
                    filename = user.profile_image.split("/")[-1]
                    delete_image(filename, "flask-blog/user")
                data = upload_image(profile_image, "flask-blog/user")

            user.name = name
            user.email = email
            if data and "secure_url" in data:
                user.profile_image = data.get("secure_url")

            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for("user.profile"))
        except IntegrityError as ex:
            violated_field = str(ex.orig).split(".")[1].split(" ")[0]
            print(violated_field)
            db.session.rollback()
            if violated_field == "email":
                flash(f"User with this email already exists!", "danger")
        except Exception as ex:
            print(str(ex))
            db.session.rollback()

    return render_template("user/profile.html", form=form, user=user)


@user_blueprint.route("/posts", methods=["GET"])
@login_required
def user_posts():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 3, type=int)
    posts = Post.query.filter_by(user_id=current_user.id).order_by(
        Post.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return render_template("user/user_posts.html", posts=posts)
