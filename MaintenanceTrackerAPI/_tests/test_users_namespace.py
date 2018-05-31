from flask_testing import TestCase

from MaintenanceTrackerAPI import create_app as create
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.auth import Login
from MaintenanceTrackerAPI.api.v1.models.request_model import requests_list
from MaintenanceTrackerAPI.api.v1.models.user_model import Admin, Consumer, users_list
from MaintenanceTrackerAPI.api.v1.users.single_user_all_requests import SingleUserAllRequests


class UsersNamespaceTestCase(TestCase):
    def create_app(self):
        app = create('testing')
        return app

    def setUp(self):
        users_list.clear()
        self.client = self.create_app().test_client()
        self.consumer = Consumer('consumer@company.com', 'password.Pa55word', 'What is your favourite company?',
                                 'company')
        self.admin = Admin('admin@company.com', 'password.Pa55word', 'What is your favourite company?',
                           'company')
        requests_list.clear()

    def login(self, data: dict):
        self.client.post(api_v1.url_for(Login), data=str(data), content_type='application/json')

    def make_request(self, data: dict, user_id: int):
        return self.client.post(api_v1.url_for(SingleUserAllRequests, user_id=user_id),
                                data=str(data), content_type='application/json')

    def tearDown(self):
        pass


class GetRequestsTestCase(UsersNamespaceTestCase):

    def test_endpoint_is_defined(self):
        response = self.client.get(api_v1.url_for(SingleUserAllRequests, user_id=1))
        self.assert200(response)


class MakeRequestsTestCase(UsersNamespaceTestCase):

    def test_login_is_required_to_make_request(self):
        response = self.make_request({'a': 'b'}, 1)
        self.assert401(response)

    def test_logged_in_consumer_can_make_request(self):
        data = dict(email='consumer@company.com', password='password.Pa55word')
        self.login(data)
        data = dict(request_type='Repair', title='Laptop Repair',
                    description='My laptop fell in water. The screen is black but I can hear sound')
        response = self.make_request(data, self.consumer.id)
        self.assertEqual(201, response.status_code)

    def test_logged_in_admin_cannot_make_request(self):
        data = dict(email='admin@company.com', password='password.Pa55word')
        self.login(data)
        data = dict(request_type='Repair', title='Laptop Repair',
                    description='My laptop fell in water. The screen is black but I can hear sound')
        response = self.make_request(data, self.admin.id)
        self.assertEqual(403, response.status_code)

    def test_consumer_makes_request_with_invalid_title(self):
        data = dict(email='consumer@company.com', password='password.Pa55word')
        self.login(data)
        data = dict(request_type='Repair', title='Laptop Repair;;',
                    description='My laptop fell in water. The screen is black but I can hear sound')
        response = self.make_request(data, self.consumer.id)
        self.assertEqual(400, response.status_code)

    def test_consumer_makes_request_with_invalid_description(self):
        data = dict(email='consumer@company.com', password='password.Pa55word')
        self.login(data)
        data = dict(request_type='Repair', title='Laptop Repair',
                    description='My laptop fell in water. The screen is black but I can hear sound;\'')
        response = self.make_request(data, self.consumer.id)
        self.assertEqual(400, response.status_code)
