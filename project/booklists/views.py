from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.booklists.models import Book
from project.users.models import User, Booklist
from project.booklists.forms import BooklistForm, EditBooklistForm
from project.bookshelves.forms import EditBookshelfForm
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
        nyt_review_url=request.form['nyt_review_url'] 
      )
      # check if this book is already in the database - if it is, don't add it
      found_book = Book.query.filter_by(title=new_book.title).filter_by(author=new_book.author)
      if found_book.count() > 0:
        book_to_add=found_book.first()
      else:
        # only if not in the database already
        db.session.add(new_book)
        db.session.commit()
        book_to_add=new_book
      new_booklist = Booklist(
        list_type='booklist',
        comments=request.form['comments'],
        rating=1,
        review='',
        user=user,
        book=book_to_add
      )
      db.session.add(new_booklist)
      db.session.commit()
      # test = db.session.query(Booklist).filter_by(user=user).filter_by(book=new_book)
      # from IPython import embed; embed()
      flash("Book added successfully!")
      return redirect(url_for('booklists.index', user_id=user_id))
    flash("Please try again")
    return render_template('booklists/new.html', form=form, user=user)
  all_books = Booklist.query.filter_by(user=user).filter_by(list_type="booklist").all()
  return render_template('booklists/index.html', form=form, user=user, books=all_books)


@booklists_blueprint.route('/new')
@login_required
@ensure_correct_user
def new(user_id):
  form = BooklistForm(request.form)
  user = User.query.get_or_404(user_id)
  return render_template('booklists/new.html', form=form, user=user)

@booklists_blueprint.route('/<int:book_id>', methods=["POST","PATCH","DELETE"])
@login_required
@ensure_correct_user
def show(user_id, book_id):
  book = Book.query.get_or_404(book_id)
  user = User.query.get_or_404(user_id)
  if request.method== "POST":
    form = EditBooklistForm(request.form)
    if form.validate():
      new_booklist = Booklist(
        list_type='booklist',
        comments=request.form['comments'],
        rating=1,
        review='',
        user=user,
        book=book
      )
      db.session.add(new_booklist)
      db.session.commit()
      flash("Book added successfully!")
      return redirect(url_for('booklists.index', user_id=user_id))
    flash("Please try again")
    return render_template('booklists/new.html', form=form, user=user)
  
  booklist = Booklist.query.filter_by(user=user).filter_by(book=book).first()
  if request.method == b"PATCH":
    form = EditBooklistForm(request.form)
    if form.validate():
      # make it so they can only update the comments OR move to their bookshelf!!!!!
      booklist.comments = request.form['comments']
      db.session.add(booklist)
      db.session.commit()
      flash("Book successfully updated")
      return redirect(url_for('booklists.index', user_id=user_id))
  if request.method == b"DELETE":
    form = EditBooklistForm(request.form)
    if form.validate():
      db.session.delete(booklist)
      db.session.delete(book)
      db.session.commit()
      flash("Book successfully removed from your booklist")
      return redirect(url_for('booklists.index', user_id=user_id))

@booklists_blueprint.route('/<int:book_id>', methods=["GET"])
@login_required
# @ensure_correct_user
def show_get(user_id, book_id):
  book = Book.query.get_or_404(book_id)
  user = User.query.get_or_404(user_id)
  booklist = Booklist.query.filter_by(user=user).filter_by(book=book).first()
  full_bookshelf = Booklist.query.filter_by(book=book).filter_by(list_type="bookshelf").all()
  average_rating = sum([b.rating for b in full_bookshelf])/len([b.rating for b in full_bookshelf])
  if booklist.user.id !=  current_user.id:
    form = EditBooklistForm(request.form)
  else:
    form = EditBookshelfForm(request.form)
  return render_template('booklists/show.html', book=booklist, form=form, user=user, full_bookshelf=full_bookshelf, average_rating=average_rating)

@booklists_blueprint.route('/<int:book_id>/edit')
@login_required
@ensure_correct_user
def edit(user_id, book_id):
  # Need to think about how to let them move a book to their bookshelf!!!!!!
  book = Book.query.get_or_404(book_id)
  user = User.query.get_or_404(user_id)
  form = EditBooklistForm(request.form)
  return render_template('booklists/edit.html', book=book, form=form, user=user)
