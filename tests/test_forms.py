#Checked
import unittest
from app import create_app, db
from app.forms import Registration, LoginForm, DirectoriesForm, FileForm
from config import TestConfig

# Test ok
class LoginFormTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app = self.app.test_client()
        self.app_context.push()

    def tearDown(self):
        db.session.rollback()
        db.session.close()
        self.app_context.pop()

    def create_login_form_user(self):
        self.form = LoginForm()
        self.form.name.data = 'Ivan'
        self.form.password.data = '12345'
        self.form.checkbox.data = False
        self.form.submit.data = True
        return self.form

    def test_form_login_user(self):
        self.form = self.create_login_form_user()
        self.assertEqual(self.form.name.data, 'Ivan')
        self.assertEqual(self.form.password.data, '12345')
        self.assertEqual(self.form.checkbox.data, False)
        self.assertEqual(self.form.submit.data, True)

    def test_to_json_login(self):
        self.form = self.create_login_form_user()
        json_form = self.form.form_to_json()
        another_form = {
            'name': 'Ivan',
            'password': '12345',
            'checkbox': False,
            'submit': True
        }
        for key in json_form:
            self.assertEqual(json_form[key].data, another_form[key])

# Test ok
class RegistrationFormTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app = self.app.test_client()
        self.app_context.push()

    def tearDown(self):
        db.session.rollback()
        db.session.close()
        self.app_context.pop()

    def create_form_user(self):
        self.form = Registration()
        self.form.username.data = 'Ivan'
        self.form.password.data = '12345'
        self.form.password_repeat.data = '12345'
        self.form.submit.data = True
        return self.form

    def test_form_user(self):
        self.form = self.create_form_user()
        self.assertEqual(self.form.username.data, 'Ivan')
        self.assertEqual(self.form.password.data, self.form.password_repeat.data)
        self.assertEqual(self.form.submit.data, True)

    def test_to_json_registration(self):
        self.form = self.create_form_user()
        json_form = self.form.form_to_json()
        another_form = {
            'username': 'Ivan',
            'password': '12345',
            'password_repeat': '12345',
            'submit': True
        }
        for key in json_form:
            self.assertEqual(json_form[key].data, another_form[key])

# Test ok
class DirectoriesFormFormTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app = self.app.test_client()
        self.app_context.push()

    def tearDown(self):
        db.session.rollback()
        db.session.close()
        self.app_context.pop()


    def create_form_directory(self):
        self.form = DirectoriesForm()
        self.form.name.data = 'First directory'
        self.form.description.data = 'Some description about'
        self.form.submit.data = True
        return self.form

    def test_form_directory(self):
        self.form = self.create_form_directory()
        self.assertEqual(self.form.name.data, 'First directory')
        self.assertEqual(self.form.description.data, 'Some description about')
        self.assertEqual(self.form.submit.data, True)

    def test_to_json_directory(self):
        self.form = self.create_form_directory()
        json_form = self.form.form_to_json()
        another_form = {
            'name': 'First directory',
            'description': 'Some description about',
            'submit': True
        }
        for key in json_form:
            self.assertEqual(json_form[key].data, another_form[key])

# Test ok
class FileFormFormFormTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app = self.app.test_client()
        self.app_context.push()

    def tearDown(self):
        db.session.rollback()
        db.session.close()
        self.app_context.pop()

    def create_file_form(self):
        self.form = FileForm()
        self.form.file.data = 'File.extend'
        self.form.submit.data = True
        return self.form

    def test_form_file(self):
        self.form = self.create_file_form()
        self.assertEqual(self.form.file.data, 'File.extend')
        self.assertEqual(self.form.submit.data, True)

    def test_to_json_file(self):
        self.form = self.create_file_form()
        json_form = self.form.form_to_json()
        another_form = {
            'file': 'File.extend',
            'submit': True
        }
        for key in json_form:
            self.assertEqual(json_form[key].data, another_form[key])


if __name__ == '__main__':
    unittest.main()