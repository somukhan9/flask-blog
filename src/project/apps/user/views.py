from sqlite3 import IntegrityError
from flask import Blueprint, render_template, flash, redirect, request, url_for, jsonify
from flask_login import current_user, login_required, login_user, logout_user

from sqlalchemy.exc import IntegrityError

from .forms import SignUpForm, LoginForm


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

    form = SignUpForm(request.form)
    if request.method == "POST":
        print("POST SUBMITTED!")
    if request.method == "POST" and form.validate_on_submit():
        print("---------------hello from post--------------------")
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


@user_blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    return render_template("user/profile.html")
