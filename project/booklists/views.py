from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.booklists.models import Book
from project.users.models import User, Booklist
from project.booklists.forms import BooklistForm
from project import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_required
from functools import wraps

booklists_blueprint = Blueprint(
  'booklists',
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

@booklists_blueprint.route('/', methods=["GET","POST"])
@login_required
def index(user_id):
  user = User.query.get_or_404(user_id)
  form = BooklistForm(request.form)
  if request.method == "POST":
    if form.validate():
      new_book = Book(
        title=request.form['title'],
        author=request.form['author'], 
        categories=request.form['categories'], 
        snippet=request.form['snippet'], 
        description=request.form['description'], 
        pages=request.form['pages'], 
        image_url=request.form['image_url'], 
        preview_url=request.form['preview_url'], 
        date_published=request.form['date_published'], 
      )
      db.session.add(new_book)
      if (request.form['list_type'] == "booklist"):
        new_booklist = Booklist(
          list_type='booklist',
          comments=request.form['comments'],
          rating='',
          review='',
          user=user,
          book=new_book
        )
        db.session.add(new_booklist)
      else: 
        new_bookshelf = Booklist(
          list_type='bookshelf',
          comments='',
          rating=request.form['rating'],
          review=request.form['review'],
          user=user,
          book=new_book
        )
        db.session.add(new_bookshelf)
      db.session.commit()
     # test = db.session.query(Booklist).filter_by(user=user).filter_by(book=new_book)
      # from IPython import embed; embed()
      flash("Book successfully added to your booklist")
      return redirect(url_for('booklists.index', user_id=user_id))
    flash("Please correct errors shown and resubmit")
    return render_template('booklists/new.html', form=form, user=user)
  return render_template('booklists/index.html', form=form, user=user)

@booklists_blueprint.route('/new')
@login_required
@ensure_correct_user
def new(user_id):
  form = BooklistForm(request.form)
  user = User.query.get_or_404(user_id)
  return render_template('booklists/new.html', form=form, user=user)

@booklists_blueprint.route('/<int:book_id>', methods=["GET","PATCH","DELETE"])
@login_required
@ensure_correct_user
def show(user_id, book_id):
  book = Book.query.get_or_404(book_id)
  user = User.query.get_or_404(user_id)
  form = BooklistForm(request.form)
  if request.method == b"PATCH":
    if form.validate():
      # make it so they can only update the comments OR move to their bookshelf!!!!!
      book.comments = request.form('comments')
      db.session.add(book)
      db.session.commit()
      flash("Book successfully updated")
      return redirect(url_for('booklists.index', user_id=user_id))
  if request.method == b"DELETE":
    if form.validate():
      db.session.delete(book)
      db.session.commit()
      flash("Book successfully removed from your booklist")
      return redirect(url_for('booklists.index', user_id=user_id))
  return render_template('booklists/show.html', book=book, form=form, user=user)

@booklists_blueprint.route('/<int:book_id>/edit')
@login_required
@ensure_correct_user
def edit(user_id, book_id):
  # Need to think about how to let them move a book to their bookshelf!!!!!!
  book = Book.query.get_or_404(book_id)
  user = User.query.get_or_404(user_id)
  form = BooklistForm(request.form)
  return render_template('booklists/edit.html', book=book, form=form, user=user)
