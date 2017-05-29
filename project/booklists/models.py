from project import db, bcrypt
from flask_login import UserMixin

class Book(db.Model, UserMixin):

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    categories = db.Column(db.Text)
    snippet = db.Column(db.Text)
    description = db.Column(db.Text)
    pages = db.Column(db.Integer)
    image_url = db.Column(db.Text)
    preview_url = db.Column(db.Text)
    date_published = db.Column(db.Text)

    def __init__(self, title, author, categories, snippet, description, pages, image_url, preview_url, date_published):
        self.title = title
        self.author = author
        self.categories = categories
        self.snippet = snippet
        self.description = description
        self.pages = pages
        self.image_url = image_url
        self.preview_url = preview_url
        self.date_published = date_published
 
    def __repr__(self):
        return "Book #{}: {} by {} - on {}".format(self.id, self.title, self.author, self.list_type)
