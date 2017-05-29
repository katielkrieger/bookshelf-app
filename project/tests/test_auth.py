import unittest
from flask_testing import TestCase
from project import app, db, bcrypt
from project.users.models import User
from flask_login import current_user
from flask import request


class TestUser(TestCase):
    def setUp(self):
    # """Disable CSRF, initialize a sqlite DB and seed a user"""
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db'
        db.create_all()
        user = User("eschoppik", "secret", "Elie S", "elie@elie.com")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """drop the db after each test"""
        db.drop_all()
   
    def test_user_registeration(self):
    # """Ensure user can register"""
        with self.client:
            response = self.client.post('/signup', data=dict(
                username='tigarcia',password='moxies',name="Tim",email="tim@tim.com"
            ), follow_redirects=True)
            self.assertIn(b'Welcome!', response.data)
            self.assertTrue(current_user.username == "tigarcia")
            # make sure we hash the password!
            self.assertNotEqual(current_user.password, "moxies")
            self.assertTrue(current_user.is_authenticated)

    # def test_incorrect_user_registeration_duplicate_username(self):
    # # """# Errors are thrown during an incorrect user registration"""
    #     with self.client:
    #         response = self.client.post('/signup', data=dict(
    #             username='eschoppik',password='doesnotmatter',name="anything",email="anything@gmail.com"))
    #         self.assertIn(b'Username has been taken', response.data)
    #         self.assertIn('/signup', request.url)

    # def test_get_by_id(self):
    # # """Ensure id is correct for the current/logged in user"""
    #     with self.client:
    #         self.client.post('/login', data=dict(
    #             username="admin", password='admin'
    #         ), follow_redirects=True)
    #         self.assertTrue(current_user.id == 1)
    #         self.assertFalse(current_user.id == 20)

    # def test_check_password(self):
    # # """ Ensure given password is correct after unhashing """
    #     user = User.query.filter_by(username='admin').first()
    #     self.assertTrue(bcrypt.check_password_hash(user.password, 'admin'))
    #     self.assertFalse(bcrypt.check_password_hash(user.password, 'notadmin'))

    # def test_login_page_loads(self):
    # # """Ensure that the login page loads correctly"""
    #     response = self.client.get('/login')
    #     self.assertIn(b'Please login', response.data)

    # def test_correct_login(self):
    # # """User should be authenticated upon successful login and stored in current user"""
    #     with self.client:
    #         response = self.client.post(
    #             '/login',
    #             data=dict(username="eschoppik", password="secret"),
    #             follow_redirects=True
    #         )
    #         self.assertIn(b'Welcome!', response.data)
    #         self.assertTrue(current_user.username == "eschoppik")
    #         self.assertTrue(current_user.is_authenticated)

    # def test_incorrect_login(self):
    # # """The correct flash message is sent when incorrect info is posted"""
    #     response = self.client.post(
    #         '/login',
    #         data=dict(username="dsadsa", password="dsadsadsa"),
    #         follow_redirects=True
    #     )
    #     self.assertIn(b"Username and password don't match", response.data)

    # def test_logout(self):
    # # """Make sure log out actually logs out a user"""
    #     with self.client:
    #         self.client.post(
    #             '/login',
    #             data=dict(username="eschoppik", password="secret"),
    #             follow_redirects=True
    #         )
    #         response = self.client.get('/logout', follow_redirects=True)
    #         self.assertIn(b'You are now logged out', response.data)
    #         self.assertFalse(current_user.is_authenticated)

    # def test_logout_route_requires_login(self):
    # # """Make sure that you can not log out without being logged in"""
    #     response = self.client.get('/logout', follow_redirects=True)
    #     self.assertIn(b'Please log in to access this page', response.data)

if __name__ == '__main__':
    unittest.main()
    