import unittest
from app import create_app, db
from config import TestConfig
from app.models import Directories, UploadedFiles, User, Role
from werkzeug.security import generate_password_hash


# Test ok
class DirectoriesTestCase(unittest.TestCase):
    '''
    For this application has been created default user in test database (TestConfig)
    name: "Default@default"
    password: "12345"
    '''

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app = self.app.test_client()
        self.app_context.push()
        self.create_directory()

    def tearDown(self):
        self.delete_directory()
        db.session.rollback()
        db.session.close()
        self.app_context.pop()

    def create_directory(self):
        self.directory = Directories(name='Directory name', description='Directory description',
                                     user_id_value=1)
        db.session.add(self.directory)
        db.session.commit()

    def delete_directory(self):
        '''
        Delete test row in table
        :return: None
        '''
        directory = Directories.query.filter_by(name='Directory name').first()
        db.session.delete(directory)
        db.session.commit()

    def test_directory_in_database(self):
        '''
        Checking for the row existing in table
        :return: None
        '''
        directory = Directories.query.filter_by(name='Directory name').first()
        self.assertFalse(directory is None)
        self.assertTrue(directory.name == 'Directory name')
        self.assertTrue(directory.description == 'Directory description')
        self.assertTrue(directory.user_id_value == 1)
        self.assertEqual(directory.__repr__(), f'<Directories {directory.id}>')
        self.assertFalse(directory.__repr__() == f'<Directories more words {directory.id}>')
        self.assertFalse(directory.description == 'Another description')
        self.assertFalse(directory.name == 'Another name')
        self.assertFalse(directory.user_id_value == 3)

    def test_directory_to_json(self):
        directory = Directories.query.filter_by(name='Directory name').first()
        another_form = {'id': directory.id,
                        'name': 'Directory name',
                        'description': 'Directory description',
                        'date': directory.date,
                        'user_id_value': 1
                        }
        json_directory = directory.to_json()
        for key in json_directory:
            self.assertEqual(json_directory[key], another_form[key])


# Test ok
class UploadedFilesTestCase(unittest.TestCase):
    '''
        For this application has been created default directory in test database (TestConfig)
        id: 30
        name: 'Defaul directory name'
        description: 'Defaul directory description'
        date: '2021-01-01 00:00:00'
        user_id_value: 1
        '''

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app = self.app.test_client()
        self.app_context.push()
        self.create_file()

    def tearDown(self):
        self.delete_file()
        db.session.rollback()
        db.session.close()
        self.app_context.pop()

    def create_file(self):
        self.file = UploadedFiles(name='File.extend', parent_id_value=30,
                                  name_to_download='Default@default' + 'File.extend')
        db.session.add(self.file)
        db.session.commit()

    def delete_file(self):
        '''
        Delete test row in table
        :return: None
        '''
        directory = UploadedFiles.query.filter_by(name='File.extend').first()
        db.session.delete(directory)
        db.session.commit()

    def test_file_in_database(self):
        '''
        Checking for the row existing in table
        :return: None
        '''
        file = UploadedFiles.query.filter_by(name='File.extend').first()
        self.assertFalse(file is None)
        self.assertTrue(file.name == 'File.extend')
        self.assertTrue(file.parent_id_value == 30)
        self.assertTrue(file.name_to_download == 'Default@defaultFile.extend')
        self.assertEqual(file.__repr__(), f'<UploadedFiles {file.id}>')
        self.assertFalse(file.__repr__() == f'<UploadedFiles more words {file.id}>')
        self.assertFalse(file.name == 'Another file name.extend')
        self.assertFalse(file.name_to_download == 'Another name')
        self.assertFalse(file.parent_id_value == 3)

    def test_file_to_json(self):
        file = UploadedFiles.query.filter_by(name='File.extend').first()
        another_form = {
            'id': file.id,
            'download_count': 0,
            'name': 'File.extend',
            'date': file.date,
            'parent_id_value': 30,
            'name_to_download': 'Default@defaultFile.extend'
        }
        json_file = file.to_json()
        for key in json_file:
            self.assertEqual(json_file[key], another_form[key])


# Test ok
class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app = self.app.test_client()
        self.app_context.push()
        self.create_user()

    def tearDown(self):
        self.delete_user()
        db.session.rollback()
        db.session.close()
        self.app_context.pop()

    def create_user(self):
        self.user = User(name='Test@test', password=generate_password_hash('12345'), role=1)
        db.session.add(self.user)
        db.session.execute(f"CREATE USER testtest WITH PASSWORD '{self.user.password}'")
        db.session.execute('GRANT user_role TO testtest')
        db.session.commit()

    def delete_user(self):
        '''
        Delete test row in table and role of user
        :return: None
        '''
        user = User.query.filter_by(name='Test@test').first()
        db.session.execute('DROP ROLE testtest')
        db.session.delete(user)
        db.session.commit()

    def connect_to_database_my_func(self):
        user = User.query.filter_by(name='Test@test').first()
        return user.connect_to_database(database_name='flask_test_database')

    def test_user_in_database(self):
        '''
        Checking for the row existing in table
        :return: None
        '''
        user = User.query.filter_by(name='Test@test').first()
        self.assertFalse(user is None)
        self.assertEqual(user.name, 'Test@test')
        self.assertEqual(user.role, 1)
        self.assertEqual(user.__repr__(), f"<User(id='{user.id}', name='{user.name}', password='{user.password}')>")
        self.assertFalse(user.__repr__() == f'<User(id={user.id}, name={user.name},'
                                            f' password={user.password}, more information)>')
        self.assertFalse(user.name == 'Another@name')

    def test_rolename_user(self):
        user = User.query.filter_by(name='Test@test').first()
        self.assertEqual(user.role_name(), 'testtest')

    def test_user_to_json(self):
        user = User.query.filter_by(name='Test@test').first()
        another_form = {
            'username': 'Test@test',
            'role': 1,
            'role_name': 'testtest'
        }
        json_user = user.to_json()
        for key in json_user:
            self.assertEqual(json_user[key], another_form[key])

