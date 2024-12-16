from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

CATEGORIES = [('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')]

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    is_active = BooleanField('Active', default=True)
    category = SelectField('Category', choices=[('Technology', 'Technology'), ('Lifestyle', 'Lifestyle')])
    publish_date = DateField('Publish Date', format='%Y-%m-%d', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('Submit')