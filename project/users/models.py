from project import db, bcrypt
from flask_login import UserMixin
from project.booklists.models import Book


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    name = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.name = name
        self.email = email

    def __repr__(self):
        return "User #{}: username: {} (email: {})".format(self.id, self.username, self.email)


class Booklist(db.Model, UserMixin):

    __tablename__ = 'booklists'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete="cascade"))
    list_type = db.Column(db.Text)
    comments = db.Column(db.Text)
    rating = db.Column(db.Integer)
    review = db.Column(db.Text)

    user = db.relationship(User, backref="booklists")
    book = db.relationship(Book, backref="booklists")

    def __init__(self, list_type, comments, rating, review, user, book):
        self.list_type = list_type
        self.comments = comments
        self.rating = rating
        self.review = review
        self.user = user
        self.book = book

    def __repr__(self):
        return "Book {} on {}'s list".format(self.book.title, self.user.username)
