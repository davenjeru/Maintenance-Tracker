from MaintenanceTrackerAPI._tests import BaseTestCase, db
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.auth import Register

db.drop_all()
db.create_all()


class RegisterTestCase(BaseTestCase):

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

    def test_consumer_register_pass(self):
        """
        Test that a consumer can be created without specifying 'role'
        :return: None
        """
        password_tuple = ('password.Pa55word', 'password.Pa55word')
        security_tuple = ('What is your favourite company?', 'company')

        response = self.register('consumer2@company.com', password_tuple,
                                 security_tuple)
        self.assertEqual(201, response.status_code)
        self.assertIn(b'Consumer', response.data)
        self.assertIn(b'user registered successfully', response.data)

        # try to create consumer again with the same email address
        response = self.register('consumer2@company.com', password_tuple,
                                 security_tuple)
        self.assertIn(b'user with similar email exists', response.data)
        self.assert400(response)

    def test_admin_register_pass(self):
        """
        Test that an Administrator is created when the role
         is specified as 'Administrator'
        :return: None
        """
        password_tuple = ('password.Pa55word', 'password.Pa55word')
        security_tuple = ('What is your favourite company?', 'company')

        response = self.register('admin2@company.com', password_tuple,
                                 security_tuple, role='Administrator')
        self.assertEqual(201, response.status_code)
        self.assertIn(b'Admin', response.data)
        self.assertIn(b'user registered successfully', response.data)

        # try to create administrator again with the same email address
        response = self.register('admin2@company.com', password_tuple,
                                 security_tuple)
        self.assertIn(b'user with similar email exists', response.data)
        self.assert400(response)

    def test_register_missing_parameter(self):
        """
        Test that user cannot be created when a parameter is missing
        :return: None
        """
        response = self.register('email@company.com')
        self.assert400(response)
        self.assertIn(b'missing', response.data)

    def test_register_invalid_password(self):
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

    def test_register_passwords_no_match(self):
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
