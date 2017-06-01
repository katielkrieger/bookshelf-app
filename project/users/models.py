from project import db, bcrypt
from flask_login import UserMixin
from project.booklists.models import Book


FollowersFollowee = db.Table('follows',
                              db.Column('id',
                                        db.Integer,
                                        primary_key=True),
                              db.Column('followee_id',
                                        db.Integer,
                                        db.ForeignKey('users.id', ondelete="cascade")),
                              db.Column('follower_id',
                                        db.Integer,
                                        db.ForeignKey('users.id', ondelete="cascade")),
                              db.CheckConstraint('follower_id != followee_id', name="no_self_follow"))


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    followers = db.relationship("User",
                              secondary=FollowersFollowee,
                              primaryjoin=(FollowersFollowee.c.followee_id == id),
                              secondaryjoin=(FollowersFollowee.c.follower_id == id),
                              backref=db.backref('following', lazy='dynamic'),
                              lazy='dynamic')
    all_followers = db.relationship("User",
                              secondary=FollowersFollowee,
                              primaryjoin=(FollowersFollowee.c.followee_id == id),
                              secondaryjoin=(FollowersFollowee.c.follower_id == id),
                              backref=db.backref('all_following', lazy='joined'),
                              lazy='joined')

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.name = name
        self.email = email

    def __repr__(self):
        return "User #{}: username: {} (email: {})".format(self.id, self.username, self.email)

    def is_followed_by(self, user):
        return bool(self.followers.filter_by(id=user.id).first())

    def is_following(self, user):
        return bool(self.following.filter_by(id=user.id).first())

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
