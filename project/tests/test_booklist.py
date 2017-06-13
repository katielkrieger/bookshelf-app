import unittest
from flask_testing import TestCase
from project import app, db
from project.users.models import User, Booklist
from project.booklists.models import Book
from flask_login import current_user


class TestUser(TestCase):

    def _login_user(self,username,password,follow_redirects=False):
        return self.client.post('/users/login',
            data=dict(username=username,
            password=password), follow_redirects=follow_redirects)


    def create_app(self):
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_ECHO"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db' 
        return app       

    def setUp(self):
        """Disable CSRF, initialize a sqlite DB and seed a user"""
        db.create_all()
        user = User("eschoppik", "secret", "Elie S", "elie@elie.com")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """drop the db after each test"""
        db.drop_all()

    def test_add_to_booklist(self):
        """Ensure user can add a book to their booklist"""
        with self.client:
            self._login_user('eschoppik','secret')
            response = self.client.post('/users/1/booklists/', data=dict(
                title="The Kite Runner",author="Khaled Hosseini",categories="Fiction",
                snippet="Afghanistan, 1975: Twelve-year-old Amir is desperate to win the local kite-fighting tournament and his loyal friend Hassan promises to help him.",
                description="Over 21 million copies sold worldwide",pages="336",
                image_url="http://books.google.com/books/content?id=MH48bnzN0LUC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                preview_url="http://books.google.com/books?id=MH48bnzN0LUC&printsec=frontcover&dq=kiterunner&hl=&cd=1&source=gbs_api",
                date_published="2011-09-05",
                nyt_review_url="dummy.com",
                comments="Here are my comments about the book."
            ), follow_redirects=True)
            self.assertIn(b'Book added successfully!', response.data)
            book = Book.query.filter_by(title="The Kite Runner").first()
            booklist = Booklist.query.filter_by(user=current_user).filter_by(book=book).first()
            # from IPython import embed; embed()
            self.assertTrue(booklist.book.author == "Khaled Hosseini")
            self.assertTrue(booklist.list_type == "booklist")
            # make sure we hash the password!
            self.assertNotEqual(booklist.book.author, "Anyone else")

    def test_modify_booklist(self):
        """Ensure user can modify a book on their booklist"""
        with self.client:
            self._login_user('eschoppik','secret')
            self.client.post('/users/1/booklists/', data=dict(
                title="The Kite Runner",author="Khaled Hosseini",categories="Fiction",
                snippet="Afghanistan, 1975: Twelve-year-old Amir is desperate to win the local kite-fighting tournament and his loyal friend Hassan promises to help him.",
                description="Over 21 million copies sold worldwide",pages="336",
                image_url="http://books.google.com/books/content?id=MH48bnzN0LUC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                preview_url="http://books.google.com/books?id=MH48bnzN0LUC&printsec=frontcover&dq=kiterunner&hl=&cd=1&source=gbs_api",
                date_published="2011-09-05",
                nyt_review_url="dummy.com",
                comments="Here are my comments about the book."
            ), follow_redirects=True)
            # confirmed that book.id = 1
            response = self.client.post('/users/1/booklists/1?_method=PATCH' , data= dict(
                comments="Here are my new comments."
            ), follow_redirects=True)
            self.assertIn(b'Book successfully updated', response.data)
            book = Book.query.filter_by(title="The Kite Runner").first()
            booklist = Booklist.query.filter_by(user=current_user).filter_by(book=book).first()
            self.assertTrue(booklist.comments == "Here are my new comments.")
            self.assertTrue(booklist.list_type == "booklist")
            # make sure we hash the password!
            self.assertNotEqual(booklist.comments, "Here are my comments about the book.")

    def test_delete_booklist(self):
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
                nyt_review_url="dummy.com",
                comments="Here are my comments about the book."
            ), follow_redirects=True)
            # confirmed that book.id = 1
            response = self.client.post('/users/1/booklists/1?_method=DELETE', follow_redirects=True)
            self.assertIn(b'Book successfully removed from your booklist', response.data)
            book = Book.query.filter_by(title="The Kite Runner").first()
            booklist = Booklist.query.filter_by(user=current_user).filter_by(book=book).first()
            self.assertFalse(booklist)

    def test_cannot_modify_another_users_booklist(self):
        """Ensure user can't modify another user's booklist comments"""
        with self.client:
            self._login_user('eschoppik','secret')
            self.client.post('/users/1/booklists/', data=dict(
                title="The Kite Runner",author="Khaled Hosseini",categories="Fiction",
                snippet="Afghanistan, 1975: Twelve-year-old Amir is desperate to win the local kite-fighting tournament and his loyal friend Hassan promises to help him.",
                description="Over 21 million copies sold worldwide",pages="336",
                image_url="http://books.google.com/books/content?id=MH48bnzN0LUC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                preview_url="http://books.google.com/books?id=MH48bnzN0LUC&printsec=frontcover&dq=kiterunner&hl=&cd=1&source=gbs_api",
                date_published="2011-09-05",
                nyt_review_url="dummy.com",
                comments="Here are my comments on the book."
            ), follow_redirects=True)
            # confirmed that book.id = 1
            user2 = User("kkrieger", "also-secret", "Katie K", "katie@katie.com")
            db.session.add(user2)
            db.session.commit()
            self._login_user('kkrieger','also-secret')
            response = self.client.post('/users/1/booklists/1?_method=PATCH' , data= dict(
                comments="Here are updated comments."
            ), follow_redirects=True)
            self.assertIn(b'Not authorized', response.data)
            book = Book.query.filter_by(title="The Kite Runner").first()
            self._login_user('eschoppik','secret')
            booklist = Booklist.query.filter_by(user=current_user).filter_by(book=book).first()
            self.assertTrue(booklist.comments == "Here are my comments on the book.")
            self.assertNotEqual(booklist.comments, "Here are updated comments.")

    def test_cannot_delete_another_users_booklist(self):
        """Ensure user can't delete another user's booklist comments"""
        with self.client:
            self._login_user('eschoppik','secret')
            self.client.post('/users/1/booklists/', data=dict(
                title="The Kite Runner",author="Khaled Hosseini",categories="Fiction",
                snippet="Afghanistan, 1975: Twelve-year-old Amir is desperate to win the local kite-fighting tournament and his loyal friend Hassan promises to help him.",
                description="Over 21 million copies sold worldwide",pages="336",
                image_url="http://books.google.com/books/content?id=MH48bnzN0LUC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                preview_url="http://books.google.com/books?id=MH48bnzN0LUC&printsec=frontcover&dq=kiterunner&hl=&cd=1&source=gbs_api",
                date_published="2011-09-05",
                nyt_review_url="dummy.com",
                comments="Here are my comments on the book."
            ), follow_redirects=True)
            # confirmed that book.id = 1
            user2 = User("kkrieger", "also-secret", "Katie K", "katie@katie.com")
            db.session.add(user2)
            db.session.commit()
            self._login_user('kkrieger','also-secret')
            response = self.client.post('/users/1/booklists/1?_method=DELETE', follow_redirects=True)
            self.assertIn(b'Not authorized', response.data)
            book = Book.query.filter_by(title="The Kite Runner").first()
            self._login_user('eschoppik','secret')
            booklist = Booklist.query.filter_by(user=current_user).filter_by(book=book).first()
            self.assertTrue(booklist)

if __name__ == '__main__':
    unittest.main()
