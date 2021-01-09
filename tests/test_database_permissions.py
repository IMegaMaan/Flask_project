import unittest
from app import create_app, db
from config import TestConfig
from app.models import Directories, UploadedFiles, User, Role


class UserTestCase(unittest.TestCase):
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

    def tearDown(self):
        db.session.close()
        self.app_context.pop()

        # Создать тесты выданных разрешений на роль user_role

    def test_connect_permissions(self):
        test_user = User.query.filter_by(name='Default@default').first()
        user_session = test_user.connect_to_database(database_name='flask_test_database')
        user_id = test_user.id
        # check user_session
        self.assertTrue(user_session)
        # create test directory by 'user_role'
        directory = Directories(name='Test directory', description='No description', user_id_value=user_id)
        user_session.add(directory)
        user_session.commit()
        # create file in database
        new_id_directory = directory.id
        file = UploadedFiles(name='Test file.test_extend', parent_id_value=new_id_directory,
                             name_to_download='Test@testTest file.test_extend')
        user_session.add(file)
        user_session.commit()
        file = user_session.query(UploadedFiles).filter_by(name='Test file.test_extend').first()
        # check file in database
        self.assertTrue(file)
        self.assertEqual(file.name, 'Test file.test_extend')
        self.assertEqual(file.name_to_download, 'Test@testTest file.test_extend')
        # check directory in database
        self.assertTrue(directory)
        self.assertEqual(directory.name, 'Test directory')
        self.assertEqual(directory.description, 'No description')
        # Close user connection
        user_session.delete(file)
        user_session.delete(directory)
        user_session.commit()
        user_session.close()
