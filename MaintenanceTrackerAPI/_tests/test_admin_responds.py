from MaintenanceTrackerAPI._tests import BaseTestCase, db
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.auth import Login
from MaintenanceTrackerAPI.api.v1.exceptions import UserTransactionError, \
    RequestTransactionError
from MaintenanceTrackerAPI.api.v1.models.request_model import Request
from MaintenanceTrackerAPI.api.v1.models.user_model import User
from MaintenanceTrackerAPI.api.v1.requests import SingleRequestAction

db.drop_all()
db.create_all()


class AdminRespondsToRequestsTestCase(BaseTestCase):

    def login(self, data: dict):
        """
        Helper function for logging in a user.
        :param data: A dictionary containing data necessary for logging in
        :return: response object
        """
        try:
            User('adminrespondstorequests@consumer.com', 'password.Pa55word',
                 'What is your favourite company?', 'Company')
            User('adminrespondstorequests@admin.com', 'password.Pa55word',
                 'What is your favourite company?', 'Company',
                 'Administrator')
        except UserTransactionError:
            pass

        response = self.client.post(api_v1.url_for(Login), data=str(data),
                                    content_type='application/json')
        response_dict = eval(response.data.decode('UTF-8'))
        access_token = response_dict.get('access_token', None)
        return access_token

    def respond_to_requests(self, action: str, logged_in: bool = True,
                            admin=False):
        """
        Helper function for making a request via the server.
        :param action: The response the admin is giving to this request
        :param admin: What user role should be used
        :param logged_in: Whether a user should be logged in or not
        :return: response object
        """

        if admin:
            email = 'adminrespondstorequests@admin.com'
        else:
            email = 'adminrespondstorequests@consumer.com'

        access_token = self.login(dict(email=email,
                                       password='password.Pa55word'))

        try:
            Request(
                dict(
                    user_id=
                    db.get_user_by_email(
                        'adminrespondstorequests@consumer.com')[
                        'user_id'],
                    email='editrequets@consumer.com',
                    role='Consumer'),
                'Repair', 'My Request Title', 'An explanation of what happened '
                                              'to justify this request.'
            )
        except RequestTransactionError:
            pass
        if logged_in:
            return self.client.put(api_v1.url_for(SingleRequestAction,
                                                  request_id=1,
                                                  action=action),
                                   content_type='application/json',
                                   headers={
                                       'ACCESS_TOKEN':
                                           access_token})
        else:
            return self.client.put(api_v1.url_for(SingleRequestAction,
                                                  request_id=1,
                                                  action=action),
                                   content_type='application/json')

    def test_admin_responds_to_request_requires_login(self):
        """
        Test that this route requires login
        :return:
        """
        response = self.respond_to_requests('approve', logged_in=False)
        self.assert401(response)

    def test_admin_responds_to_request_pass(self):
        """
        Test that an admin can view one request
        :return:
        """
        response = self.respond_to_requests('approve', admin=True)
        self.assertIn(b'Approved', response.data)
        self.assert200(response)

        response = self.respond_to_requests('approve', admin=True)
        self.assertIn(b'Cannot', response.data)

        response = self.respond_to_requests('resolve', admin=True)
        self.assertIn(b'Resolved', response.data)

    def test_consumer_responds_to_request_fail(self):
        """
        Test that a consumer cannot use this route
        :return:
        """
        response = self.respond_to_requests('disapprove', admin=False)
        self.assert403(response)

    def test_admin_responds_to_request_pfail(self):
        """
        Test that an admin can view one request
        :return:
        """
        response = self.respond_to_requests('possos', admin=True)
        self.assertIn(b'not recognized', response.data)

        response = self.respond_to_requests('approve', admin=True)
        self.assertIn(b'Cannot', response.data)
