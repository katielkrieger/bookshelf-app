from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, URL, AnyOf
from wtforms.widgets import TextArea


class BooklistForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    categories=StringField('categories') 
    snippet=StringField('snippet') 
    description=StringField('description')  
    pages=StringField('pages')  
    image_url=StringField('image_url', validators=[URL()])  
    preview_url=StringField('preview_url', validators=[URL()])  
    date_published=StringField('date_published')  
    comments = StringField('comments', widget=TextArea())
    rating = IntegerField('rating', validators=[NumberRange(min=1, max=10)])
    review = StringField('review', widget=TextArea())
