from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, AnyOf
from wtforms.widgets import TextArea


class BookshelfForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    categories=StringField('categories') 
    snippet=StringField('snippet') 
    description=StringField('description')  
    pages=StringField('pages')  
    image_url=StringField('image_url')  
    preview_url=StringField('preview_url')  
    date_published=StringField('date_published')  
    # comments = StringField('comments', widget=TextArea())
    rating = IntegerField('rating', validators=[NumberRange(min=1, max=10)])
    review = StringField('review', widget=TextArea())

class EditBookshelfForm(FlaskForm):
    rating = IntegerField('rating', validators=[NumberRange(min=1, max=10)])
    review = StringField('review', widget=TextArea())