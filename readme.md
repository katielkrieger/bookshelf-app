# My Bookshelves

## About

With [this web app](https://my-bookshelves.herokuapp.com), users can keep track of books they want to read, and can rate and review books they have read. 

Books that a user wants to read are saved on their *booklist*. Similarly, books they have read and reviewed go on their *bookshelf*. A user's reviews are shown on their home page in an interactive D3 visualization.

Users can add books to their booklist or bookshelf using a search functionality. They can also mark books on their booklist as read. Doing so allows them to rate and review the book, and moves it from their booklist to their bookshelf.

Users can browse the top rated books on the site and email their reviews to a friend using a simple form. Users can also follow other users and explore the top rated books of the people they follow. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This app's dependencies are listed in `requirements.txt`. 

### Installing

* Make a virtual environment: `mkvirtualenv <NAME>`.
* Make the `solo-project` database: `createdb solo-project`.
* Pip install the requirements: `pip install -r requirements.txt`.
* Upgrade the database to set up the tables: `python manage.py db upgrade`.

## Running the tests

Unit tests are located in `projects/tests`. To run all the tests as once, type `green` in the root of the project.

To run a specific tests (if you want to debug with iPython):
`python -m project.tests.<name_of_test>`.

## Deployment

To deploy this on a live system, follow the instructions [here](https://devcenter.heroku.com/articles/getting-started-with-python#introduction).


## Built With

* [JavaScript](https://www.javascript.com/) - Used for client-side development
* [Python](https://www.python.org/) - Used for server-side development
* [Flask](http://flask.pocoo.org/) - Python microframework
* [D3.js](https://github.com/d3/d3/) - Used to vizualize book reviews
* [Flask Mail](https://pythonhosted.org/Flask-Mail/) - Used to send email recommendations
* [Flask Modus](https://pypi.python.org/pypi/Flask-Modus/0.0.1) - Used to make PATCH and DELETE requests
* [Flask Login](https://flask-login.readthedocs.io/en/latest/) - Used for user authentication and authorization
* [Flask-WTF](http://flask.pocoo.org/docs/0.12/patterns/wtforms/) - Used for form creation
* [SQLAlchemy](https://www.sqlalchemy.org/) - Used for database manipulation
* [jQuery](http://jquery.com/) - Used to manipulate the DOM and make AJAX calls
* [Bootstrap](http://getbootstrap.com/2.3.2/) - Used for page layout and responsive design
* [Slick](http://kenwheeler.github.io/slick/) - Used for photo carousel on landing page
* CSS
* HTML

## Contributing

When contributing to this repository, please first discuss the change you wish to make with the owner of this repository before making a change.

## Versioning

Git was used for versioning. For the versions available, see this repository.

## Authors

* **Katie Krieger**

## License

This project is licensed under the MIT License.

Copyright 2017 Katie Krieger

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Acknowledgements

* Special thanks to Elie, Matt, and Tim at [Rithm School](http://rithmschool.com/) for their support and guidance.
* Thank you to [Google Books](https://developers.google.com/books/) for its Google Books API, which provided book metadata for this app.
* Thank you to the [New York Times](http://developer.nytimes.com.) for its API, which was used to provide links to New York Times book reviews.
* Thank you to [Slick](http://kenwheeler.github.io/slick/) for the photo carousel.


