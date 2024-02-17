import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_ckeditor import CKEditor


# Loading the environment variables
load_dotenv()


app = Flask(
    __name__,
    static_url_path="/root-static"
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "SQLALCHEMY_DATABASE_URI", "sqlite:///project.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "super-secret-key")

# Initializing Database
db = SQLAlchemy(app)

# Enabling Migrate Feature to SQLALchemy
migrate = Migrate(app, db)

# Initializing Login Manager for user authentication
login_manager = LoginManager(app)

# Setting the default login view for Login Manager
login_manager.login_view = "user.login"

# Enabling CKEditor
ckeditor = CKEditor(app)


# Importing here to avoid "circular import issue"
from project.apps.user.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Registered Blog Blueprint
from project.apps.blog.views import blog_blueprint
app.register_blueprint(blog_blueprint, url_prefix="")

# Registered User Blueprint
from project.apps.user.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix="/user")


@app.route('/go_back')
def go_back():
    # Get the referring URL using request.referrer
    referring_url = request.referrer

    # If the referring URL is None or is the current URL, redirect to the home page
    # if referring_url is None or referring_url == request.url:
    #     return redirect(url_for('home'))

    # Redirect to the referring URL
    return redirect(referring_url)


@app.errorhandler(404)
def error_404(e):
    return render_template("404.html")


@app.errorhandler(500)
def error_500(e):
    return render_template("500.html")
