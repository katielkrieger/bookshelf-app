from flask import Flask, render_template, url_for, request, redirect
from project.booklists.forms import BooklistForm
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)

if os.environ.get('ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'postgres://localhost/solo-project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or "who knows"

modus = Modus(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.booklists.views import booklists_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(booklists_blueprint, url_prefix='/users/<int:user_id>/booklists')

from project.users.models import User

login_manager.init_app(app)
login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def root():
    return redirect(url_for('users.index'))

