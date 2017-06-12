from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
import os

app = Flask(__name__)

if os.environ.get('ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'postgres://localhost/solo-project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True # I would make sure to make this false when in production
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or "who knows"
app.config.update(dict(
    DEBUG = True, ## Also probably something you want to make false in prod
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'mybookshelvesapp@gmail.com',
    MAIL_PASSWORD = 'webinarz',
    ADMINS = ['katielkrieger@gmail.com']
))
app.jinja_env.auto_reload = True # Definitely want to make this false in prod

modus = Modus(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)
mail = Mail(app)

from project.users.views import users_blueprint
from project.booklists.views import booklists_blueprint
from project.bookshelves.views import bookshelves_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(booklists_blueprint, url_prefix='/users/<int:user_id>/booklists')
app.register_blueprint(bookshelves_blueprint, url_prefix='/users/<int:user_id>/bookshelves')

from project.users.models import User, Booklist

login_manager.init_app(app)
login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def root():
    if current_user.is_anonymous:
        return render_template('home.html')
    else:
        following = current_user.all_following
        following_ids = [f.id for f in following]
        bookshelves = Booklist.query.filter(Booklist.user_id.in_(following_ids)).order_by("rating desc").limit(120).all()
        return redirect(url_for('users.index', books=bookshelves))
