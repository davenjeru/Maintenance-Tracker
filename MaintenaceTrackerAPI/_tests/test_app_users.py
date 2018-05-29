from flask_testing import TestCase

from MaintenaceTrackerAPI import app
from MaintenaceTrackerAPI.api.v1 import api_v1
from MaintenaceTrackerAPI.api.v1.users import UsersAllRequests, UsersSingleRequests


class AppTestCase(TestCase):
    def create_app(self):
        app.testing = True
        return app

    def setUp(self):
        self.client = self.create_app().test_client()

    def tearDown(self):
        pass

    def test_a1_no_base_index(self):
        response = self.client.get('/')
        self.assert404(response)

    def test_a2_api_index(self):
        response = self.client.get(api_v1.base_url)
        self.assert200(response)

    def test_a3_User_Views_All_Requests(self):
        response = self.client.get(api_v1.url_for(UsersAllRequests))
        self.assertIn(b'requests', response.data)

    def test_a4_User_View_Single_Request(self):
        response = self.client.get(api_v1.url_for(UsersSingleRequests, request_id=1))
        self.assertIn(b'request', response.data)

    def test_a5_User_Creates_Request(self):
        response = self.client.post(api_v1.url_for(UsersAllRequests))
        self.assertEqual(201, response.status_code)

    def test_a6_User_Modifies_Request(self):
        response = self.client.put(api_v1.url_for(UsersSingleRequests, request_id=1))
        self.assert200(response)
