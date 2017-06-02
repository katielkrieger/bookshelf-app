# My Bookshelves

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This app's dependencies are listed in `requirements.txt`. To install all dependencies through the terminal, `cd` to the directory where `requirements.txt` is located. Activate your virtual environment, and run `pip install -r requirements.txt` in the terminal.

### Installing

1. (Google books images and preview links are on http, but my heroku site is on https, so it's complaining about that.)
2. Add tests for followers, following.
3. Write readme.

## Running the tests

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

## Deployment

* DONE - Showing a NYT book review on the book show pages
* DONEish - Parallax home page
* DONE - Add a test to check password reset
* NOT NEEDED - Remove duplicates from the book search
* DONE - The ability to follow other users and see their booklists/bookshelves
* DONE - A D3 vizualization using the book metadata collected
* DONE - The ability to see all reviews by users you are following when you click on a book's show page
* DONE - The ability to send a specific user or email address a book recommendation

## Built With

* Flask - The microframework used
* 

## Contributing

## Versioning

## Authors

## License

## Acknowledgements

* Special thanks to Elie, Matt, and Tim at [Rithm School](http://rithmschool.com/)
* Thank you to [Google Books](https://developers.google.com/books/) for its Google Books API, which provided book metadata for this app
* Thank you to the [New York Times](http://developer.nytimes.com.) for its API, which was used to provide links to New York Times book reviews.


