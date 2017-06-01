from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.users.models import User, Booklist
from project.users.forms import UserForm, UpdateForm, LogInForm, UpdatePasswordForm
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
    form = UserForm(request.form)
    if request.method == "POST":
        if form.validate():
            try:
                new_user = User(
                    request.form['username'], 
                    request.form['password'], 
                    request.form['name'], 
                    request.form['email']
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                flash("Welcome {}!".format(new_user.username))
                return redirect(url_for('users.index'))
            except IntegrityError as e:
                flash("Username has been taken")
                return render_template('users/signup.html', form=form)
    return render_template('users/signup.html', form=form)

@users_blueprint.route('/login', methods=["GET","POST"])
def login():
    form = LogInForm(request.form)
    if request.method == "POST":
        if form.validate():
            found_user = User.query.filter_by(username = form.username.data).first()
            if found_user:
                authenticated_user = bcrypt.check_password_hash(found_user.password, request.form['password'])
                if authenticated_user:
                    login_user(found_user)
                    flash("Welcome {}!".format(found_user.username))
                    return redirect(url_for('users.show', user_id=current_user.id))
            flash("Username and password do not match")
            return render_template('users/login.html', form=form)
    return render_template('users/login.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
    flash ("You are now logged out")
    logout_user()
    return redirect(url_for('root'))

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
    booklist = Booklist.query.filter_by(user=found_user).filter_by(list_type="booklist").all()
    bookshelf = Booklist.query.filter_by(user=found_user).filter_by(list_type="bookshelf").all()
    return render_template('users/show.html', user=found_user, booklist=booklist, bookshelf=bookshelf)

@users_blueprint.route('/<int:user_id>/edit')
@login_required
@ensure_correct_user
def edit(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(request.form)
    return render_template('users/edit.html', form=form, user=user)

@users_blueprint.route('/<int:user_id>/edit_password', methods=["GET", "PATCH"])
@login_required
@ensure_correct_user
def edit_password(user_id):
    found_user = User.query.get_or_404(user_id)
    if request.method == b"PATCH":
        form = UpdatePasswordForm(request.form)
        if form.validate():
            authenticated_user = bcrypt.check_password_hash(found_user.password, request.form['old_password'])
            if authenticated_user and (request.form['new_password'] == request.form['confirm_password']):
                found_user.password = bcrypt.generate_password_hash(request.form['new_password']).decode('UTF-8')
                db.session.add(found_user)
                db.session.commit()
                flash("Password updated successfully")
                return redirect(url_for('users.index'))
            flash("Passwords do not match. Please try again.")
            return render_template("users/edit_password.html", form=form, user=found_user)
        flash("Please correct errors shown and resubmit")
        return render_template("users/edit_password.html", form=form, user=found_user)
    form = UpdatePasswordForm()
    return render_template('users/edit_password.html', form=form, user=found_user)

@users_blueprint.route('/<int:follower_id>/follower', methods=['POST', 'DELETE'])
@login_required
def follower(follower_id):
  followed = User.query.get(follower_id)
  if request.method == 'POST':
    current_user.following.append(followed)
  else:
    current_user.following.remove(followed)
  db.session.add(current_user)
  db.session.commit()
  return redirect(url_for('users.following', id=current_user.id))

@users_blueprint.route('/<int:user_id>/following', methods=['GET'])
@login_required
def following(user_id):
  return render_template('users/following.html', user=User.query.get(user_id))

@users_blueprint.route('/<int:user_id>/followers', methods=['GET'])
@login_required
def followers(user_id):
  return render_template('users/followers.html', user=User.query.get(user_id))
