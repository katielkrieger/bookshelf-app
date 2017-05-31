import unittest
from flask_testing import TestCase
from project import app, db, bcrypt
from project.users.models import User, Booklist
from project.booklists.models import Book
from flask_login import current_user
from flask import request


class TestUser(TestCase):

    def _login_user(self,username,password,follow_redirects=False):
        return self.client.post('/users/login',
            data=dict(username=username,
            password=password), follow_redirects=follow_redirects)


    def create_app(self):
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db' 
        return app       

    def setUp(self):
    # """Disable CSRF, initialize a sqlite DB and seed a user"""
        db.create_all()
        user = User("eschoppik", "secret", "Elie S", "elie@elie.com")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """drop the db after each test"""
        db.drop_all()

    # def testAddToBooklist(self):
    #     """Ensure user can add a book to their booklist"""
    #     with self.client:
    #         self._login_user('eschoppik','secret')
    #         response = self.client.post('/users/1/booklists/', data=dict(
    #             title="The Kite Runner",author="Khaled Hosseini",categories="Fiction",
    #             snippet="Afghanistan, 1975: Twelve-year-old Amir is desperate to win the local kite-fighting tournament and his loyal friend Hassan promises to help him.",
    #             description="Over 21 million copies sold worldwide",pages="336",
    #             image_url="http://books.google.com/books/content?id=MH48bnzN0LUC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
    #             preview_url="http://books.google.com/books?id=MH48bnzN0LUC&printsec=frontcover&dq=kiterunner&hl=&cd=1&source=gbs_api",
    #             date_published="2011-09-05",
    #             comments="Here are my comments about the book."
    #         ), follow_redirects=True)
    #         self.assertIn(b'Book added successfully!', response.data)
    #         book = Book.query.filter_by(title="The Kite Runner").first()
    #         booklist = Booklist.query.filter_by(user=current_user).filter_by(book=book).first()
    #         # from IPython import embed; embed()
    #         self.assertTrue(booklist.book.author == "Khaled Hosseini")
    #         self.assertTrue(booklist.list_type == "booklist")
    #         # make sure we hash the password!
    #         self.assertNotEqual(booklist.book.author, "Anyone else")

    # def testAddToBookshelf(self):
    #     """Ensure user can add a book to their bookshelf"""
    #     with self.client:
    #         self._login_user('eschoppik','secret')
    #         response = self.client.post('/users/1/bookshelves/', data=dict(
    #             title="The Kite Runner, 2nd ed",author="Khaled Hosseini",categories="Fiction",
    #             snippet="Afghanistan, 1975: Twelve-year-old Amir is desperate to win the local kite-fighting tournament and his loyal friend Hassan promises to help him.",
    #             description="Over 21 million copies sold worldwide",pages="336",
    #             image_url="http://books.google.com/books/content?id=MH48bnzN0LUC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
    #             preview_url="http://books.google.com/books?id=MH48bnzN0LUC&printsec=frontcover&dq=kiterunner&hl=&cd=1&source=gbs_api",
    #             date_published="2011-09-05",
    #             rating="9",
    #             review="Here is my review of the book."
    #         ), follow_redirects=True)
    #         self.assertIn(b'Book added successfully!', response.data)
    #         book = Book.query.filter_by(title="The Kite Runner, 2nd ed").first()
    #         booklist = Booklist.query.filter_by(user=current_user).filter_by(book=book).first()
    #         # from IPython import embed; embed()
    #         self.assertTrue(booklist.book.author == "Khaled Hosseini")
    #         self.assertTrue(booklist.list_type == "bookshelf")
    #         # make sure we hash the password!
    #         self.assertNotEqual(booklist.book.author, "Anyone else")

    # def testModifyBooklist(self):
    #     """Ensure user can modify a book on their booklist"""
    #     with self.client:
    #         self._login_user('eschoppik','secret')
    #         self.client.post('/users/1/booklists/', data=dict(
    #             title="The Kite Runner",author="Khaled Hosseini",categories="Fiction",
    #             snippet="Afghanistan, 1975: Twelve-year-old Amir is desperate to win the local kite-fighting tournament and his loyal friend Hassan promises to help him.",
    #             description="Over 21 million copies sold worldwide",pages="336",
    #             image_url="http://books.google.com/books/content?id=MH48bnzN0LUC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
    #             preview_url="http://books.google.com/books?id=MH48bnzN0LUC&printsec=frontcover&dq=kiterunner&hl=&cd=1&source=gbs_api",
    #             date_published="2011-09-05",
    #             comments="Here are my comments about the book."
    #         ), follow_redirects=True)
    #         # confirmed that book.id = 1
    #         response = self.client.post('/users/1/booklists/1?_method=PATCH' , data= dict(
    #             comments="Here are my new comments."
    #         ), follow_redirects=True)
    #         self.assertIn(b'Book successfully updated', response.data)
    #         book = Book.query.filter_by(title="The Kite Runner").first()
    #         booklist = Booklist.query.filter_by(user=current_user).filter_by(book=book).first()
    #         self.assertTrue(booklist.comments == "Here are my new comments.")
    #         self.assertTrue(booklist.list_type == "booklist")
    #         # make sure we hash the password!
    #         self.assertNotEqual(booklist.comments, "Here are my comments about the book.")

    # def testModifyBookshelf(self):
    #     """Ensure user can modify a book on their bookshelf"""
    #     with self.client:
    #         self._login_user('eschoppik','secret')
    #         self.client.post('/users/1/bookshelves/', data=dict(
    #             title="The Kite Runner, 2nd ed",author="Khaled Hosseini",categories="Fiction",
    #             snippet="Afghanistan, 1975: Twelve-year-old Amir is desperate to win the local kite-fighting tournament and his loyal friend Hassan promises to help him.",
    #             description="Over 21 million copies sold worldwide",pages="336",
    #             image_url="http://books.google.com/books/content?id=MH48bnzN0LUC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
    #             preview_url="http://books.google.com/books?id=MH48bnzN0LUC&printsec=frontcover&dq=kiterunner&hl=&cd=1&source=gbs_api",
    #             date_published="2011-09-05",
    #             rating="9",
    #             review="Here is my review of the book."
    #         ), follow_redirects=True)
    #         # confirmed that book.id = 1
    #         response = self.client.post('/users/1/bookshelves/1?_method=PATCH' , data= dict(
    #             rating = "3",
    #             review="Here is an updated review."
    #         ), follow_redirects=True)
    #         self.assertIn(b'Book successfully updated', response.data)
    #         book = Book.query.filter_by(title="The Kite Runner, 2nd ed").first()
    #         booklist = Booklist.query.filter_by(user=current_user).filter_by(book=book).first()
    #         self.assertTrue(booklist.rating == 3)
    #         self.assertTrue(booklist.list_type == "bookshelf")
    #         # make sure we hash the password!
    #         self.assertNotEqual(booklist.rating, 9)

    def testDeleteBooklist(self):
        """Ensure user can delete a book on their booklist"""
        with self.client:
            self._login_user('eschoppik','secret')
            self.client.post('/users/1/booklists/', data=dict(
                title="The Kite Runner",author="Khaled Hosseini",categories="Fiction",
                snippet="Afghanistan, 1975: Twelve-year-old Amir is desperate to win the local kite-fighting tournament and his loyal friend Hassan promises to help him.",
                description="Over 21 million copies sold worldwide",pages="336",
                image_url="http://books.google.com/books/content?id=MH48bnzN0LUC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                preview_url="http://books.google.com/books?id=MH48bnzN0LUC&printsec=frontcover&dq=kiterunner&hl=&cd=1&source=gbs_api",
                date_published="2011-09-05",
                comments="Here are my comments about the book."
            ), follow_redirects=True)
            # confirmed that book.id = 1
            response = self.client.post('/users/1/booklists/1?_method=DELETE', follow_redirects=True)
            self.assertIn(b'Book successfully removed from your booklist', response.data)
            book = Book.query.filter_by(title="The Kite Runner").first()
            booklist = Booklist.query.filter_by(user=current_user).filter_by(book=book).first()
            self.assertFalse(booklist)

    # def testDeleteBookshelf(self):
    #     """Ensure user can delete a book on their bookshelf"""
    #     with self.client:
    #         self._login_user('eschoppik','secret')
    #         self.client.post('/users/1/bookshelves/', data=dict(
    #             title="The Kite Runner",author="Khaled Hosseini",categories="Fiction",
    #             snippet="Afghanistan, 1975: Twelve-year-old Amir is desperate to win the local kite-fighting tournament and his loyal friend Hassan promises to help him.",
    #             description="Over 21 million copies sold worldwide",pages="336",
    #             image_url="http://books.google.com/books/content?id=MH48bnzN0LUC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
    #             preview_url="http://books.google.com/books?id=MH48bnzN0LUC&printsec=frontcover&dq=kiterunner&hl=&cd=1&source=gbs_api",
    #             date_published="2011-09-05",
    #             rating="9",
    #             comments="Here is my review of the book."
    #         ), follow_redirects=True)
    #         # confirmed that book.id = 1
    #         response = self.client.post('/users/1/bookshelves/1?_method=DELETE', follow_redirects=True)
    #         self.assertIn(b'Book successfully removed from your bookshelf', response.data)
    #         book = Book.query.filter_by(title="The Kite Runner").first()
    #         booklist = Booklist.query.filter_by(user=current_user).filter_by(book=book).first()
    #         self.assertFalse(booklist)

    # def test_user_registeration(self):
    # # """Ensure user can register"""
    #     with self.client:
    #         response = self.client.post('/users/signup', data=dict(
    #             username='tigarcia',password='moxies',name="Tim",email="tim@tim.com"
    #         ), follow_redirects=True)
    #         self.assertIn(b'Welcome', response.data)
    #         self.assertTrue(current_user.username == "tigarcia")
    #         # make sure we hash the password!
    #         self.assertNotEqual(current_user.password, "moxies")
    #         self.assertTrue(current_user.is_authenticated)

    # def test_incorrect_user_registeration_duplicate_username(self):
    # # """# Errors are thrown during an incorrect user registration"""
    #     with self.client:
    #         response = self.client.post('/users/signup', data=dict(
    #             username='eschoppik',password='doesnotmatter',name="anything",email="anything@gmail.com"))
    #         self.assertIn(b'Username has been taken', response.data)
    #         self.assertIn('/users/signup', request.url)

    # def test_get_by_id(self):
    # # """Ensure id is correct for the current/logged in user"""
    #     with self.client:
    #         self.client.post('/users/login', data=dict(
    #             username="eschoppik", password='secret'
    #         ), follow_redirects=True)
    #         self.assertTrue(current_user.id == 1)
    #         self.assertFalse(current_user.id == 20)

    # def test_check_password(self):
    # # """ Ensure given password is correct after unhashing """
    #     user = User.query.filter_by(username='eschoppik').first()
    #     self.assertTrue(bcrypt.check_password_hash(user.password, 'secret'))
    #     self.assertFalse(bcrypt.check_password_hash(user.password, 'notsecret'))

    # def test_login_page_loads(self):
    # # """Ensure that the login page loads correctly"""
    #     response = self.client.get('/users/login')
    #     self.assertIn(b'Please login', response.data)

    # def test_correct_login(self):
    # # """User should be authenticated upon successful login and stored in current user"""
    #     with self.client:
    #         response = self.client.post(
    #             '/users/login',
    #             data=dict(username="eschoppik", password="secret"),
    #             follow_redirects=True
    #         )
    #         self.assertIn(b'Welcome', response.data)
    #         self.assertTrue(current_user.username == "eschoppik")
    #         self.assertTrue(current_user.is_authenticated)

    # def test_incorrect_login(self):
    # # """The correct flash message is sent when incorrect info is posted"""
    #     response = self.client.post(
    #         '/users/login',
    #         data=dict(username="dsadsa", password="dsadsadsa"),
    #         follow_redirects=True
    #     )
    #     self.assertIn(b"Username and password do not match", response.data)

    # def test_logout(self):
    # # """Make sure log out actually logs out a user"""
    #     with self.client:
    #         self.client.post(
    #             '/users/login',
    #             data=dict(username="eschoppik", password="secret"),
    #             follow_redirects=True
    #         )
    #         response = self.client.get('/users/logout', follow_redirects=True)
    #         self.assertIn(b'You are now logged out', response.data)
    #         self.assertFalse(current_user.is_authenticated)

    # def test_logout_route_requires_login(self):
    # # """Make sure that you can not log out without being logged in"""
    #     response = self.client.get('/users/logout', follow_redirects=True)
    #     self.assertIn(b'Please log in to access this page', response.data)

    # def testEditPassword(self):
    # # Logged In User Editing Password
    #     self._login_user('eschoppik','secret')
    #     response = self.client.post('/users/1/edit_password?_method=PATCH',
    #         data=dict(new_password='newpass', confirm_password='newpass',
    #         old_password='secret'), follow_redirects=True)
    #     user = User.query.filter_by(username='eschoppik').first()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(bcrypt.check_password_hash(user.password, 'newpass'),True)

if __name__ == '__main__':
    unittest.main()
