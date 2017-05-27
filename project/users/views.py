from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.users.models import User
from project.users.forms import UserForm, LoginForm
from project import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps

users_blueprint = Blueprint(
  'users',
  __name__,
  template_folder='templates'
)

@users_blueprint.route('/', methods=["GET","POST"])
def index():
    if request.method == "POST":
        form = OwnerForm()
        if form.validate_on_submit():
            new_user = User(request.form['username'], request.form['password'], request.form['name'], request.form['email'])
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('users.index'))
        return render_template('users/new.html', form=form)
    return render_template('users/index.html', users=User.query.all())

@users_blueprint.route('/signup', methods=["GET"])
def new():
    form = UserForm()
    return render_template('users/new.html', form=form)

# @users_blueprint.route('/login', methods=["GET","POST"])
# def login():
#     pass

# @users_blueprint.route('/logout')
# def logout():
#     pass

@users_blueprint.route('<int:user_id>/edit')
def edit(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm()
    return render_template('users/edit.html', form=form, user=user)

@users_blueprint.route('<int:user_id>', methods=["GET","PATCH","DELETE"])
def show(user_id):
    pass
