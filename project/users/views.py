from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.users.models import User
from project.users.forms import UserForm, UpdateForm, LogInForm
from project import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps

users_blueprint = Blueprint(
  'users',
  __name__,
  template_folder='templates'
)

def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get('user_id') != current_user.id:
            flash("Not authorized")
            return redirect(url_for('users.index'))
        return fn(*args, **kwargs)
    return wrapper

@users_blueprint.route('/')
def index():
    return render_template('users/index.html', users=User.query.all())

@users_blueprint.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserForm()
    if form.validate_on_submit():
        try:
            new_user = User(request.form['username'], request.form['password'], request.form['name'], request.form['email'])
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
        except IntegrityError as e:
            flash("Username has been taken")
            return render_template('users/signup.html', form=form)
        return redirect(url_for('users.index'))
    return render_template('users/signup.html', form=form)

@users_blueprint.route('/login', methods=["GET","POST"])
def login():
    form = LogInForm(request.form)
    if form.validate_on_submit():
        found_user = User.query.filter_by(username = form.username.data).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(found_user.password, request.form['password'])
            if authenticated_user:
                login_user(found_user)
                flash("Welcome!")
                return redirect(url_for('users.index'))
    if form.is_submitted():
        flash("Username and password don't match")
    return render_template('users/login.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
    flash ("You are now logged out")
    logout_user()
    return redirect(url_for('users.login'))

@users_blueprint.route('/<int:user_id>', methods=["GET","PATCH","DELETE"])
@login_required
def show(user_id):
    found_user = User.query.get_or_404(user_id)
    if request.method == b"PATCH":
        form = UpdateForm(request.form)
        if form.validate():
            found_user.username = request.form['username']
            found_user.name = request.form['name']
            found_user.email = request.form['email']
            db.session.add(found_user)
            db.session.commit()
            return redirect(url_for('users.index'))
        return render_template("users/edit.html", form=form, user=found_user)
    if request.method == b"DELETE":
        db.session.delete(found_user)
        db.session.commit()
        return redirect(url_for('users.index'))
    return render_template('users/show.html', user=found_user)

@users_blueprint.route('/<int:user_id>/edit')
@login_required
@ensure_correct_user
def edit(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm()
    return render_template('users/edit.html', form=form, user=user)

