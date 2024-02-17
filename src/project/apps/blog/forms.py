# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FileField, SelectField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from wtforms_sqlalchemy.fields import QuerySelectField

from project.apps.blog.models import Category


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = CKEditorField('Body', validators=[
                         DataRequired()])
    summary = TextAreaField('Summary', validators=[DataRequired()])
    featured_image = FileField('Featured Image', validators=[DataRequired()])
    category = QuerySelectField("Select Category", query_factory=lambda: Category.query.all(
    ), allow_blank=True, get_label="title", blank_text="Select Category", validators=[DataRequired()],
        blank_value="disabled",
    )
