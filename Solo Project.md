# Solo Project Notes


##File names for reference:

* File path: `Rithm/Heroku/Full Books App`
* Virtual env: `solo-project`
* Database: `solo-project`
* Heroku app name : TBD
* GitHub repo: TBD

## General resources

* Blueprints [here](https://github.com/rithmschool/python_curriculum/blob/master/Unit-02/01-blueprints.md)
* Testing [here](https://github.com/rithmschool/python_curriculum/blob/master/Unit-02/04-flask_login.md)

## Basic features

* CRUD app with three resources: users, booklists, and bookshelves
* Authentication for users
* The ability to add books using search by title or author (using the Google Books API)
* The book list has a button to mark a book as read and add a review
* Prevent the same book from being on a user's booklist and bookshelf
* Tests are built and passing for the basic functionality
* App is deployed on Heroku
* App is styled with Bootstrap
* Include a README which explains how to get the app running locally, what technologies you've used, and why you decided to build the project
* Links to Github and Heroku are [here](https://github.com/rithmschool/fullstack_project/blob/master/applications.md)

## Bonus features

* Showing a NYT book review on the book show pages
* The ability to follow other users and see their booklists/bookshelves
* A D3 vizualization using the book metadata collected
* The ability to see all reviews by users you are following when you click on a book's show page
* The ability to send a specific user or email address a book recommendation

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