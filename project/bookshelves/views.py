from flask import redirect, render_template, request, url_for, Blueprint, flash
from flask_mail import Message
from project.booklists.models import Book
from project.users.models import User, Booklist
from project.bookshelves.forms import BookshelfForm, EditBookshelfForm, EmailForm
from project.booklists.forms import EditBooklistForm
from project import db, bcrypt, mail
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from flask_login import current_user, login_required
from functools import wraps

bookshelves_blueprint = Blueprint(
  'bookshelves',
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

@bookshelves_blueprint.route('/', methods=["GET","POST"])
@login_required
def index(user_id):
  user = User.query.get_or_404(user_id)
  form = BookshelfForm(request.form)
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
      new_bookshelf = Booklist(
        list_type='bookshelf',
        comments='',
        rating=request.form['rating'],
        review=request.form['review'],
        user=user,
        book=book_to_add
      )
      db.session.add(new_bookshelf)
      db.session.commit()
      flash("Book added successfully!")
      return redirect(url_for('bookshelves.index', user_id=user_id))
    flash("Please try again")
    return render_template('bookshelves/new.html', form=form, user=user)
  all_books = Booklist.query.filter_by(user=user).filter_by(list_type="bookshelf").all()
  # Look into N+1 query issue
  return render_template('bookshelves/index.html', form=form, user=user, books=all_books)


@bookshelves_blueprint.route('/new')
@login_required
@ensure_correct_user
def new(user_id):
  form = BookshelfForm(request.form)
  user = User.query.get_or_404(user_id)
  return render_template('bookshelves/new.html', form=form, user=user)

@bookshelves_blueprint.route('/<int:book_id>', methods=["PATCH","DELETE"])
@login_required
@ensure_correct_user
def show(user_id, book_id):
  book = Book.query.get_or_404(book_id)
  user = User.query.get_or_404(user_id)
  bookshelf = Booklist.query.filter_by(user=user).filter_by(book=book).first()
  form = EditBookshelfForm(request.form)
  if request.method == b"PATCH":
    if form.validate():
      bookshelf.rating = request.form['rating']
      bookshelf.review = request.form['review']
      bookshelf.list_type = "bookshelf"
      db.session.add(bookshelf)
      db.session.commit()
      flash("Book successfully updated")
      return redirect(url_for('bookshelves.index', user_id=user_id))
  if request.method == b"DELETE":
    if form.validate():
      db.session.delete(bookshelf)
      # db.session.delete(book)
      db.session.commit()
      flash("Book successfully removed from your bookshelf")
      return redirect(url_for('bookshelves.index', user_id=user_id))

@bookshelves_blueprint.route('/<int:book_id>', methods=["GET"])
@login_required
# @ensure_correct_user
def show_get(user_id, book_id):
  book = Book.query.get_or_404(book_id)
  user = User.query.get_or_404(user_id)
  bookshelf = Booklist.query.filter_by(user=user).filter_by(book=book).first()
  full_bookshelf = Booklist.query.filter_by(book=book).filter_by(list_type="bookshelf").all()
  if len([b.rating for b in full_bookshelf]) == 0:
    average_rating = "No ratings yet"
  else:
    average_rating = round(sum([b.rating for b in full_bookshelf])/len([b.rating for b in full_bookshelf]),1)
  if bookshelf.user.id !=  current_user.id:
    form = EditBooklistForm(request.form)
  else:
    form = EmailForm(request.form)
  return render_template('bookshelves/show.html', book=bookshelf, form=form, user=user, full_bookshelf=full_bookshelf, average_rating=average_rating)

@bookshelves_blueprint.route('/<int:book_id>/edit')
@login_required
@ensure_correct_user
def edit(user_id, book_id):
  # Need to think about how to let them move a book to their bookshelf!!!!!!
  book = Book.query.get_or_404(book_id)
  user = User.query.get_or_404(user_id)
  form = EditBookshelfForm(request.form)
  return render_template('bookshelves/edit.html', book=book, form=form, user=user)

@bookshelves_blueprint.route('/<int:book_id>/email',methods=["POST"])
@login_required
@ensure_correct_user
def email(user_id, book_id):
  form = EmailForm(request.form)
  book = Book.query.get_or_404(book_id)
  user = User.query.get_or_404(user_id)
  bookshelf = Booklist.query.filter_by(user=user).filter_by(book=book).first()
  recipients = request.form['recipient'].split(',')

  if form.validate_on_submit():
    msg = Message("Here's a book I thought you might like",
                sender=(current_user.name,current_user.email),
                recipients=recipients)
    msg.body = render_template('bookshelves/email.html', user=user, book=bookshelf)
    msg.html = render_template('bookshelves/email.html', user=user, book=bookshelf)
    mail.send(msg)
    return redirect(url_for('bookshelves.index', user_id=user.id))
  flash("Invalid email address. Please try again.")
  return render_template('bookshelves/show.html', form=form, book=bookshelf, user=user)
