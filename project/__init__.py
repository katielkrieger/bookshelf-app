from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'postgres://localhost/solo-project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or "who knows"

modus = Modus(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.users.models import User

app.register_blueprint(users_blueprint, url_prefix='/users')