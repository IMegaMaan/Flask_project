import unittest
from flask import current_app
from app import create_app, db
from config import TestConfig


class BasicsTestCase(unittest.TestCase):
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

    def test_db_is_exist(self):
        self.assertFalse(db is None)

    def test_app_is_exist(self):
        self.assertFalse(create_app(TestConfig) is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()