# Solo Project Notes


##File names for reference:

* File path: `Rithm/Heroku/Full Books App`
* Virtual env: `solo-project`
* Database: `solo-project`
* Heroku app name : `my-bookshelves` (secret key is `webinarz`)
* GitHub repo: `bookshelf-app`
* Gmail account for mail feature: username `mybookshelvesapp`, pw `webinarz`

## General resources

* Blueprints [here](https://github.com/rithmschool/python_curriculum/blob/master/Unit-02/01-blueprints.md)
* Testing [here](https://github.com/rithmschool/python_curriculum/blob/master/Unit-02/04-flask_login.md)

## Questions/Issues

1. (Google books images and preview links are on http, but my heroku site is on https, so it's complaining about that.)
2. Add tests for followers, following.
3. Write readme.

## Basic features

* CRUD app with three resources: users, booklists, and bookshelves
* Authentication for users, including opportunity to change their password
* The ability to add books using search by title or author (using the Google Books API)
* The book list has a button to mark a book as read and add a review
* Prevent the same book from being on a user's booklist and bookshelf
* Tests are built and passing for the basic functionality
* App is deployed on Heroku
* App is styled with Bootstrap
* Include a README which explains how to get the app running locally, what technologies you've used, and why you decided to build the project
* Links to Github and Heroku are [here](https://github.com/rithmschool/fullstack_project/blob/master/applications.md)

## Bonus features

* DONE - Showing a NYT book review on the book show pages
* DONEish - Parallax home page
* DONE - Add a test to check password reset
* NOT NEEDED - Remove duplicates from the book search
* DONE - The ability to follow other users and see their booklists/bookshelves
* DONE - A D3 vizualization using the book metadata collected
* DONE - The ability to see all reviews by users you are following when you click on a book's show page
* DONE - The ability to send a specific user or email address a book recommendation

## Milestone targets

* Monday - auth working, user routes set up, Heroku set up
* Tuesday - book routes added, book search working
* Wednesday - styling, navbar and testing - see photos here https://unsplash.com/search/books
* Thursday - readme, bonuses
* Friday - bonuses, finish readme, final push to Github and Heroku

## Database schema

### User table "users"
- id (primary key)
- name
- email
- password
- booklist (backref to books on booklist)
- bookshelf (backref to books on bookshelf)

### Book table "books"
Everything but the id comes from the AJAX request to Google Books API when a user searches for a book.
https://www.googleapis.com/books/v1/volumes/bKq3oAEACAAJ 
- id (primary key)
- title (`response.items[0].volumeInfo.title`)
- author (`response.items[0].volumeInfo.authors`)
- categories (`response.items[0].volumeInfo.categories`)
- text snippet (`response.items[0].searchInfo.snippet`)
- description (`response.items[0].volumeInfo.description`)
- pages (`response.items[0].volumeInfo.pageCount`)
- image link (`response.items[0].volumeInfo.imageLinks.thumbnail`)
- preview link (`response.items[0].volumeInfo.previewLink`)
- published date (`response.items[0].volumeInfo.publishedDate`)

### UserBook (M:M relationship)
- user_id (foreign key)
- book_id (foreign key)
- type (bookList or bookShelf)
- userRating (1-10) -- bookShelf only
- userReview (text) -- bookShelf only
- comments (text) -- bookList only (e.g., friend recommended it to me, or I read about it in the NYT)

## Root page

A welcome page, with links to log in or sign up, plus a link to check out the user index.

## User pages

### Index

A display of users so you can browse others to see who you might want to follow or look at. Login not required.

### New

New user sign up page.

### Show

See a user's information, including username, name, and links to their booklists and bookshelves. 

### Edit

Edit a user's account information (username, name, email), plus a link to a separate page to edit their password.

## Booklist pages

### Index

A display of all books on a user's booklist. Titles and thumbnails. Login not required.

### New

A page to add a new book to the user's booklist, using search with the Google Books API. 

### Show

A page showing a user's book, including the user's notes about why they want to read it. Also shows a photo of the book, the description, number of pages, snippet, etc. Login not required.

To access a user's book review: 
user = User.query.get_or_404(user_id)
book = Book.query.get_or_404(book_id)
user_book = db.session.query(Booklist).filter_by(user=user).filter_by(book=book)
user_book.first().rating (or comments or review)


### Edit

A page to edit a user's book notes, including an option to move it to their bookshelf, or delete it from their booklist.


## Bookshelf pages

### Index

A display of all books on a user's bookshelf. Titles and thumbnails. Login not required.

### New

A page to add a new book to the user's bookshelf, using search with the Google Books API. 

### Show

A page showing a user's book, including the user's rating and review. Also shows a photo of the book, the description, number of pages, snippet, etc. Login not required.

### Edit

A page to edit a user's book rating and/or review, or to remove it from their bookshelf.