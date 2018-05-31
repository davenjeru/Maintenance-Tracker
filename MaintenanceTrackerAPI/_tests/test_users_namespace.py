from flask_testing import TestCase

from MaintenanceTrackerAPI import create_app as create
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.auth import Login, Logout
from MaintenanceTrackerAPI.api.v1.models.request_model import requests_list
from MaintenanceTrackerAPI.api.v1.models.user_model import Admin, Consumer, users_list
from MaintenanceTrackerAPI.api.v1.users.single_user_all_requests import SingleUserAllRequests


class UsersNamespaceTestCase(TestCase):
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
        users_list.clear()
        self.client = self.create_app().test_client()
        self.consumer = Consumer('consumer@company.com', 'password.Pa55word', 'What is your favourite company?',
                                 'company')
        self.admin = Admin('admin@company.com', 'password.Pa55word', 'What is your favourite company?',
                           'company')
        requests_list.clear()

    def login(self, data: dict):
        """
        Helper function for logging in a user.
        :param data: A dictionary containing data necessary for logging in
        :return: None
        """
        self.client.post(api_v1.url_for(Login), data=str(data), content_type='application/json')

    def make_request(self, data: dict, user_id: int):
        """
        Helper function for logging in a user.
        :param data: A dictionary containing data necessary for logging in
        :param user_id: The user id that should be added to the route
        :return: None
        """
        return self.client.post(api_v1.url_for(SingleUserAllRequests, user_id=user_id),
                                data=str(data), content_type='application/json')

    def tearDown(self):
        """
        Overridden method from TestCase
        :return: None
        """
        pass


class GetRequestsTestCase(UsersNamespaceTestCase):

    def test_endpoint_is_defined(self):
        """
        Test to check whether this endpoint is defined.
        The test fails if the Resource is not registered to its namespace,
        or the Namespace is not registered to the Api
        :return: None
        """
        self.client.get(api_v1.url_for(SingleUserAllRequests, user_id=1))

    def check_login_is_required(self):
        """
        Test to check that login is required to access this Resource
        :return:
        """
        response = self.client.get(api_v1.url_for(SingleUserAllRequests, user_id=1))
        self.assert401(response)

    def test_get_all_requests_empty_list(self):
        """
        Test that the there is initially an empty list since the user has not created any requests yet
        :return: None
        """
        data = dict(email='consumer@company.com', password='password.Pa55word')
        self.login(data)
        response = self.client.get(api_v1.url_for(SingleUserAllRequests, user_id=self.consumer.id))
        self.assertIn(b'[]', response.data)

    def test_get_all_requests(self):
        """
        Test that a a list of requests is returned
        :return: None
        """
        # log the consumer in
        data = dict(email='consumer@company.com', password='password.Pa55word')
        self.login(data)

        # let the user make a request
        data = dict(request_type='Repair', title='Laptop Repair',
                    description='My laptop fell in water. The screen is black but I can hear sound')
        self.make_request(data, self.consumer.id)

        # let the user make another request
        data['title'] = 'Phone Repair'
        data['description'] = 'My phone screen has been destroyed. The screen itself and not the top glass'
        self.make_request(data, self.consumer.id)

        # check the response when a GET request is made
        response = self.client.get(api_v1.url_for(SingleUserAllRequests, user_id=self.consumer.id))
        self.assertIn(b'Phone Repair', response.data)
        self.assertIn(b'Laptop Repair', response.data)

        # logout the consumer
        self.client.post(api_v1.url_for(Logout))

        # log the admin in
        data = dict(email='admin@company.com', password='password.Pa55word')
        self.login(data)

        # check the response when a GET request is made
        response = self.client.get(api_v1.url_for(SingleUserAllRequests, user_id=self.consumer.id))
        self.assertIn(b'Phone Repair', response.data)
        self.assertIn(b'Laptop Repair', response.data)

    def test_user_cannot_view_another_users_request(self):
        """
        Test that a user cannot access another user's requests
        :return: None
        """
        another_consumer = Consumer('consumer2@company.com', 'password.Pa55word', 'What is your favourite company?',
                                    'company')
        data = dict(email='consumer@company.com', password='password.Pa55word')
        self.login(data)
        response = self.client.get(api_v1.url_for(SingleUserAllRequests, user_id=another_consumer.id))
        self.assert403(response)


class MakeRequestsTestCase(UsersNamespaceTestCase):

    def test_login_is_required_to_make_request(self):
        """
        Test that login is required to make request
        :return: None
        """
        response = self.make_request({'a': 'b'}, 1)
        self.assert401(response)

    def test_logged_in_consumer_can_make_request(self):
        """
        Test that a consumer that is logged in can make a request
        :return: None
        """
        data = dict(email='consumer@company.com', password='password.Pa55word')
        self.login(data)
        data = dict(request_type='Repair', title='Laptop Repair',
                    description='My laptop fell in water. The screen is black but I can hear sound')
        response = self.make_request(data, self.consumer.id)
        self.assertEqual(201, response.status_code)

    def test_logged_in_admin_cannot_make_request(self):
        """
        Test that an Administrator cannot make a request
        :return: None
        """
        data = dict(email='admin@company.com', password='password.Pa55word')
        self.login(data)
        data = dict(request_type='Repair', title='Laptop Repair',
                    description='My laptop fell in water. The screen is black but I can hear sound')
        response = self.make_request(data, self.admin.id)
        self.assertEqual(403, response.status_code)

    def test_consumer_makes_request_with_invalid_title(self):
        """
        Test that a request cannot be made with an invalid title
        :return: None
        """
        data = dict(email='consumer@company.com', password='password.Pa55word')
        self.login(data)
        data = dict(request_type='Repair', title='Laptop Repair;;',
                    description='My laptop fell in water. The screen is black but I can hear sound')
        response = self.make_request(data, self.consumer.id)
        self.assertEqual(400, response.status_code)

    def test_consumer_makes_request_with_invalid_description(self):
        """
        Test that a request cannot be made with an invalid description
        :return: None
        """
        data = dict(email='consumer@company.com', password='password.Pa55word')
        self.login(data)
        data = dict(request_type='Repair', title='Laptop Repair',
                    description='My laptop fell in water. The screen is black but I can hear sound;\'')
        response = self.make_request(data, self.consumer.id)
        self.assertEqual(400, response.status_code)

    def test_consumer_makes_request_with_invalid_request_type(self):
        """
        Test that a request cannot be made with an invalid request type
        :return: None
        """
        data = dict(email='consumer@company.com', password='password.Pa55word')
        self.login(data)
        data = dict(request_type='Another Type', title='Laptop Repair',
                    description='My laptop fell in water. The screen is black but I can hear sound.')
        response = self.make_request(data, self.consumer.id)
        self.assertIn(b'Cannot recognize the request type given :', response.data)

    def test_consumer_makes_request_with_none_request_type(self):
        """
        Test that a request cannot be made with request type set as None
        :return: None
        """
        data = dict(email='consumer@company.com', password='password.Pa55word')
        self.login(data)
        data = dict(request_type=None, title='Laptop Repair',
                    description='My laptop fell in water. The screen is black but I can hear sound.')
        response = self.make_request(data, self.consumer.id)
        self.assertEqual(201, response.status_code)
