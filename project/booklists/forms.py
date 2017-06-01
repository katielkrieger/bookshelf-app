from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, HiddenField
from wtforms.validators import DataRequired, NumberRange, URL, AnyOf
from wtforms.widgets import TextArea


class BooklistForm(FlaskForm):
    title = HiddenField()#StringField('title', validators=[DataRequired()])
    author = HiddenField()#StringField('author', validators=[DataRequired()])
    categories=HiddenField()#StringField('categories') 
    snippet=HiddenField()#StringField('snippet') 
    description=HiddenField()#StringField('description')  
    pages=HiddenField()#StringField('pages')  
    image_url=HiddenField()#StringField('image_url')  
    preview_url=HiddenField()#StringField('preview_url')  
    date_published=HiddenField()#StringField('date_published') 
    nyt_review_url=HiddenField() 
    comments = StringField('comments', widget=TextArea())
    # rating = IntegerField('rating', validators=[NumberRange(min=1, max=10)])
    # review = StringField('review', widget=TextArea())

class EditBooklistForm(FlaskForm):
    comments = StringField('comments', widget=TextArea())