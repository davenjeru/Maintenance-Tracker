from flask_testing import TestCase

from MaintenanceTrackerAPI import create_app as create
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.auth import Register, Logout
from MaintenanceTrackerAPI.api.v1.auth.login import Login


class AppTestCase(TestCase):
    def create_app(self):
        """
        Create the Flask application with 'testing' as the configuration
        :return: app -> the Flask app
        """
        app = create('testing')
        return app

    def setUp(self):
        """
        Set up the testing client
        :return: None
        """
        self.client = self.create_app().test_client()

    def tearDown(self):
        """
        Tasks to be done once testing is done
        :return: None
        """
        pass

    def test_no_base_index(self):
        """
        Test the root index '/' of the app
        This test fails if there was something wrong with creating the Flask app
        :return: None
        """
        response = self.client.get('/')
        self.assert404(response)

    def test_api_index(self):
        """
        Test the base url of the api(v1) '/api/v1/'
        This test fails if the Api Blueprint was not registered by the Flask app
        :return: None
        """
        response = self.client.get(api_v1.base_url)
        self.assert200(response)

    def test_not_json(self):
        """
        Test when the request lacks header lacks
         'content_type='application/json''
        :return: None
        """
        response = self.client.post(api_v1.url_for(Register))
        self.assertEqual(415, response.status_code)

    def test_no_data(self):
        """
        Test that the server checks when the request body is empty
        :return: None
        """
        response = self.client.post(api_v1.url_for(Register),
                                    content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertIn(b'no data was found in the request', response.data)

    def register(self, email: str = None, password_tuple: tuple = (None, None),
                 security_tuple: tuple = (None, None), role=None):
        """
        Helper function for registering a user to avoid code duplication
        :param email: email address of the user to be registered
        :param password_tuple: a tuple containing 'password'
         and 'confirm_password'
        :param security_tuple: a tuple containing 'security_question'
         and 'security_answer'
        :param role: 'the role that the user should be created under'
        :return: response object
        """
        data = dict(email=email)
        data['password'], data['confirm_password'] = password_tuple
        data['security_question'], data['security_answer'] = security_tuple
        data['role'] = role
        return self.client.post(api_v1.url_for(Register), data=str(data),
                                content_type='application/json')

    def test_a1_consumer_register_pass(self):
        """
        Test that a consumer can be created without specifying 'role'
        :return: None
        """
        password_tuple = ('password.Pa55word', 'password.Pa55word')
        security_tuple = ('What is your favourite company?', 'company')

        response = self.register('consumer@company.com', password_tuple,
                                 security_tuple)
        self.assertEqual(201, response.status_code)
        self.assertIn(b'Consumer', response.data)
        self.assertIn(b'user registered successfully', response.data)

        # try to create consumer again with the same email address
        response = self.register('consumer@company.com', password_tuple,
                                 security_tuple)
        self.assertIn(b'user with similar email exists', response.data)
        self.assert400(response)

    def test_a1_admin_register_pass(self):
        """
        Test that an Administrator is created when the role
         is specified as 'Administrator'
        :return: None
        """
        password_tuple = ('password.Pa55word', 'password.Pa55word')
        security_tuple = ('What is your favourite company?', 'company')

        response = self.register('admin@company.com', password_tuple,
                                 security_tuple, role='Administrator')
        self.assertEqual(201, response.status_code)
        self.assertIn(b'Admin', response.data)
        self.assertIn(b'user registered successfully', response.data)

        # try to create administrator again with the same email address
        response = self.register('admin@company.com', password_tuple,
                                 security_tuple)
        self.assertIn(b'user with similar email exists', response.data)
        self.assert400(response)

    def test_a2_register_missing_parameter(self):
        """
        Test that user cannot be created when a parameter is missing
        :return: None
        """
        response = self.register('email@company.com')
        self.assert400(response)
        self.assertIn(b'missing', response.data)

    def test_a3_register_invalid_password(self):
        """
        Test that user cannot register with the wrong password syntax
        :return: None
        """
        password_tuple = ('password', 'password')
        security_tuple = ('What is your favourite company?', 'company')
        response = self.register('email@company.com', password_tuple,
                                 security_tuple)
        self.assert400(response)
        self.assertIn(b'password syntax is invalid', response.data)

    def test_a4_register_passwords_no_match(self):
        """
        Test that 'password' and 'confirm_password' fields that do not match
         should not register user
        :return: None
        """
        password_tuple = ('password.Pa55word', 'password')
        security_tuple = ('What is your favourite company?', 'company')
        response = self.register('email@company.com', password_tuple,
                                 security_tuple)
        self.assert400(response)
        self.assertIn(b'passwords do not match', response.data)

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

    def test_a7_login(self):
        """
        Test that a user can log in.
        :return: None
        """
        email = 'consumer@company.com'
        password = 'password.Pa55word'
        response = self.login(email, password)
        self.assert200(response)
        self.assertIn(b'user logged in successfully', response.data)

        # try and log in again
        response = self.login(email, password)
        self.assert400(response)
        self.assertIn(b'currently logged in', response.data)

    def test_a8_login_fail(self):
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

    def test_a9_logout(self):
        """
        Test the logout route
        :return: None
        """
        self.login('consumer@company.com', 'password.Pa55word')
        response = self.client.post(api_v1.url_for(Logout))
        self.assert200(response)
        self.assertIn(b'logged out successfully', response.data)
        response = self.client.post(api_v1.url_for(Logout))
        self.assert400(response)
        self.assertIn(b'no user in session', response.data)
