from MaintenanceTrackerAPI._tests import BaseTestCase
from MaintenanceTrackerAPI._tests import db
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.auth import Login
from MaintenanceTrackerAPI.api.v1.exceptions import UserTransactionError
from MaintenanceTrackerAPI.api.v1.models.user_model import User
from MaintenanceTrackerAPI.api.v1.users import SingleUserAllRequests


class RequestCreationTestCase(BaseTestCase):

    def login(self, data: dict):
        """
        Helper function for logging in a user.
        :param data: A dictionary containing data necessary for logging in
        :return: response object
        """
        try:
            User('requestcreation@company.com', 'password.Pa55word',
                 'What is your favourite company?', 'Company')
            User('requestcreation@admin.com', 'password.Pa55word',
                 'What is your favourite company?', 'Company',
                 'Administrator')
        except UserTransactionError:
            pass

        response = self.client.post(api_v1.url_for(Login), data=str(data),
                                    content_type='application/json')
        response_dict = eval(response.data.decode('UTF-8'))
        access_token = response_dict.get('access_token', None)
        return access_token

    def make_request(self, data: dict, logged_in: bool = True, admin=False):
        """
        Helper function for making a request via the server.
        :param admin: What user role should be used
        :param logged_in: Whether a user should be logged in or not
        :param data: A dictionary containing data necessary for logging in
        :return: response object
        """

        if admin:
            email = 'requestcreation@admin.com'
        else:
            email = 'requestcreation@company.com'
        access_token = self.login(dict(email=email,
                                       password='password.Pa55word'))
        user_id = db.get_user_by_email(email)['user_id']
        if logged_in:
            return self.client.post(api_v1.url_for(SingleUserAllRequests,
                                                   user_id=user_id),
                                    data=str(data),
                                    content_type='application/json',
                                    headers={
                                        'ACCESS_TOKEN':
                                            access_token})
        else:
            return self.client.post(api_v1.url_for(SingleUserAllRequests,
                                                   user_id=user_id),
                                    data=str(data),
                                    content_type='application/json')

    def test_login_is_required_to_make_request(self):
        """
        Test that login is required to make request
        :return: None
        """
        response = self.make_request({'a': 'b'}, False)
        self.assert401(response)

    def test_logged_in_consumer_can_make_request(self):
        """
        Test that a consumer that is logged in can make a request
        :return: None
        """
        data = dict(request_type='Repair', title='Laptop Repair',
                    description='My laptop fell in water.'
                                ' The screen is black but I can hear sound')
        response = self.make_request(data)
        self.assertEqual(201, response.status_code)

    def test_logged_in_admin_cannot_make_request(self):
        """
        Test that an Administrator cannot make a request
        :return: None
        """
        data = dict(request_type='Repair', title='Laptop Repair',
                    description='My laptop fell in water.'
                                ' The screen is black but I can hear sound')
        response = self.make_request(data, admin=True)
        self.assertEqual(403, response.status_code)

    def test_consumer_makes_request_with_invalid_title(self):
        """
        Test that a request cannot be made with an invalid title
        :return: None
        """
        data = dict(request_type='Repair', title='Laptop Repair;;',
                    description='My laptop fell in water.'
                                ' The screen is black but I can hear sound')
        response = self.make_request(data)
        self.assertEqual(400, response.status_code)

    def test_consumer_makes_request_with_invalid_description(self):
        """
        Test that a request cannot be made with an invalid description
        :return: None
        """
        data = dict(request_type='Repair', title='Laptop Repair',
                    description='My laptop fell in water.'
                                ' The screen is black but I can hear sound;\'')
        response = self.make_request(data, True)
        self.assertEqual(400, response.status_code)

    def test_consumer_makes_request_with_invalid_request_type(self):
        """
        Test that a request cannot be made with an invalid request type
        :return: None
        """
        data = dict(request_type='Another Type', title='Laptop Repair',
                    description='My laptop fell in water.'
                                ' The screen is black but I can hear sound.')
        response = self.make_request(data)
        self.assertIn(b'Cannot recognize the request type given :',
                      response.data)

    def test_consumer_makes_request_with_none_request_type(self):
        """
        Test that a request cannot be made with request type set as None
        :return: None
        """
        data = dict(request_type=None, title='Laptop Repair',
                    description='My laptop fell in water.'
                                ' The screen is black but I can hear sound.')
        response = self.make_request(data)
        self.assertEqual(201, response.status_code)
