from project import db, bcrypt
from flask_login import UserMixin

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
        