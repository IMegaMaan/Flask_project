import unittest
from app import create_app, db
from config import TestConfig
import json
from app.forms import LoginForm


class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app.config['TESTING'] = True
        self.app.config['LOGIN_DISABLED'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app = self.app.test_client()
        self.app_context.push()

    def tearDown(self):
        db.session.rollback()
        db.session.close()
        self.app_context.pop()

    def login_form_create(self):
        data = {'name': 'Default@default', 'password': '12345', 'remember': False, 'test': True}
        return self.app.post('/login', data=data, follow_redirects=True)

    def test_valid_user_registration(self):
        response = self.login_form_create()
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.app.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_page(self):
        response = self.app.get('/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_directory_page(self):
        response = self.app.get('/create_directory', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def create_directory_data(self):
        data = json.dumps({'name': 'Unique test description', 'description': 'Some description'})
        return self.app.post('/create_directory', data=data, follow_redirects=True, content_type='application/json')


if __name__ == '__main__':
    unittest.main()
