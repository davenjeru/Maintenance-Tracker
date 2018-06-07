from MaintenanceTrackerAPI._tests import BaseTestCase, db
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.auth import Login

# clear database
db.drop_all()

# create tables
db.create_all()


class LoginTestCase(BaseTestCase):
    def login(self, email: str = None, password: str = None):
        """
        Helper class for logging in any user to avoid duplication
        :param email: the user's email address
        :param password: the user's password
        :return: None
        """
        data = dict(email=email, password=password)
        return self.client.post(api_v1.url_for(Login), data=str(data),
                                content_type='application/json')

    def test_login(self):
        """
        Test that a user can log in.
        :return: None
        """
        email = 'consumer@company.com'
        password = 'password.Pa55word'
        response = self.login(email, password)
        self.assert200(response)
        self.assertIn(b'user logged in successfully', response.data)
        self.assertIn(b'access_token', response.data)

    def test_login_fail(self):
        """
        Test that user should not log in with wrong or unknown credentials
        :return: None
        """
        email = 'consumer@company.com'
        password = 'not.a.5imilaRpass'
        response = self.login(email, password)
        self.assert401(response)
        self.assertIn(b'invalid password', response.data)

        email = 'email254@company.com'
        response = self.login(email, password)
        self.assert400(response)
        self.assertIn(b'user not found', response.data)

        response = self.login(None, password)
        self.assert400(response)
        self.assertIn(b'missing', response.data)
