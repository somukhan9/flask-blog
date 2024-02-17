from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class SignUpForm(FlaskForm):
    name = StringField("Name",
                       validators=[DataRequired(message="Please provide a name!")])
    email = EmailField("Email Address", validators=[DataRequired(
        message="Please provide a valid email address!"), Email(message="Please provide a valid email address!")])
    password = PasswordField("Password", validators=[
                             DataRequired(message="Please enter a password!"), Length(min=6, message="Password should be at least of 6 characters!")])
    password2 = PasswordField("Repeat Password", validators=[
                              DataRequired(message="Please repeat the password!"), EqualTo("password", message="Passwords did not match!")])


class LoginForm(FlaskForm):
    email = EmailField("Email Address", validators=[DataRequired(
        message="Please provide a valid email address!"), Email(message="Please provide a valid email address!")])
    password = PasswordField("Password", validators=[
                             DataRequired(message="Please give a password!")])
