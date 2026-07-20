import unittest

from app import app, db
from models import User


class AuthFlowTests(unittest.TestCase):
    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
            WTF_CSRF_ENABLED=False,
        )
        self.app_context = app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_registration_stores_password_that_can_be_checked(self):
        response = self.client.post(
            '/register',
            data={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'StrongPass1',
                'role': 'Student',
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('StrongPass1'))
        self.assertFalse(user.check_password('WrongPass'))


if __name__ == '__main__':
    unittest.main()
