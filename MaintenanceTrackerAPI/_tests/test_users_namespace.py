from flask_testing import TestCase

from MaintenanceTrackerAPI import create_app as create
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.users.single_user_all_requests import SingleUserAllRequests


class UsersNamespaceTestCase(TestCase):
    def create_app(self):
        app = create('testing')
        return app

    def setUp(self):
        self.client = self.create_app().test_client()

    def tearDown(self):
        pass


class GetRequestsTestCase(UsersNamespaceTestCase):

    def test_endpoint_is_defined(self):
        response = self.client.get(api_v1.url_for(SingleUserAllRequests, user_id=1))
        self.assert200(response)
