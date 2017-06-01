from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, HiddenField, RadioField
from wtforms.validators import DataRequired, NumberRange, AnyOf, Email
from wtforms.widgets import TextArea


class BookshelfForm(FlaskForm):
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
    rating = RadioField('rating', choices=[("1",1),("2",2),("3",3),("4",4),("5",5),("6",6),("7",7),("8",8),("9",9),("10",10)], default='1', validators=[DataRequired()])
    review = StringField('review', widget=TextArea())

class EditBookshelfForm(FlaskForm):
    rating = RadioField('rating', choices=[("1",1),("2",2),("3",3),("4",4),("5",5),("6",6),("7",7),("8",8),("9",9),("10",10)], default='1', validators=[DataRequired()])
    review = StringField('review', widget=TextArea())

class EmailForm(FlaskForm):
    recipient = StringField('email', validators=[DataRequired(), Email()])