from MaintenanceTrackerAPI._tests import BaseTestCase
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.auth import Login
from MaintenanceTrackerAPI.api.v1.exceptions import UserTransactionError
from MaintenanceTrackerAPI.api.v1.models.user_model import User
from MaintenanceTrackerAPI.api.v1.requests import AllRequests


class AdminViewAllRequestsTestCase(BaseTestCase):
    def login(self, data: dict):
        """
        Helper function for logging in a user.
        :param data: A dictionary containing data necessary for logging in
        :return: response object
        """
        try:
            User('adminviewsallrequests@consumer.com', 'password.Pa55word',
                 'What is your favourite company?', 'Company')
            User('adminviewsallrequests@admin.com', 'password.Pa55word',
                 'What is your favourite company?', 'Company',
                 'Administrator')
        except UserTransactionError:
            pass

        response = self.client.post(api_v1.url_for(Login), data=str(data),
                                    content_type='application/json')
        response_dict = eval(response.data.decode('UTF-8'))
        access_token = response_dict.get('access_token', None)
        return access_token

    def get_all_requests(self, logged_in: bool = True, admin=False):
        """
        Helper function for making a request via the server.
        :param admin: What user role should be used
        :param logged_in: Whether a user should be logged in or not
        :return: response object
        """

        if admin:
            email = 'adminviewsallrequests@admin.com'
        else:
            email = 'adminviewsallrequests@consumer.com'

        access_token = self.login(dict(email=email,
                                       password='password.Pa55word'))
        if logged_in:
            return self.client.get(api_v1.url_for(AllRequests),
                                   content_type='application/json',
                                   headers={
                                       'ACCESS_TOKEN':
                                           access_token})
        else:
            return self.client.get(api_v1.url_for(AllRequests),
                                   content_type='application/json')

    def test_admin_gets_requests_requires_login(self):
        """
        Test that this route requires login
        :return:
        """
        response = self.get_all_requests(logged_in=False)
        self.assert401(response)

    def test_admin_gets_requests_pass(self):
        """
        Test that a consumer can view their requests
        :return:
        """
        response = self.get_all_requests(admin=True)
        self.assertIn(b'requests', response.data)
        self.assert200(response)

    def test_consumer_gets_requests_fail(self):
        """
        Test that a consumer can view their requests
        :return:
        """
        response = self.get_all_requests(admin=False)
        self.assert403(response)
