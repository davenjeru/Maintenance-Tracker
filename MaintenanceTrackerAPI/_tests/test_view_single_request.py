from MaintenanceTrackerAPI._tests import BaseTestCase, db
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.auth import Login
from MaintenanceTrackerAPI.api.v1.exceptions import UserTransactionError, \
    RequestTransactionError
from MaintenanceTrackerAPI.api.v1.models.request_model import Request
from MaintenanceTrackerAPI.api.v1.models.user_model import User
from MaintenanceTrackerAPI.api.v1.users import SingleUserSingleRequest


class ViewOneRequestTestCase(BaseTestCase):
    db.drop_all()
    db.create_all()

    def login(self, data: dict):
        """
        Helper function for logging in a user.
        :param data: A dictionary containing data necessary for logging in
        :return: response object
        """
        try:
            User('viewrequest@consumer.com', 'password.Pa55word',
                 'What is your favourite company?', 'Company')
            User('viewrequest@admin.com', 'password.Pa55word',
                 'What is your favourite company?', 'Company',
                 'Administrator')
        except UserTransactionError:
            pass

        response = self.client.post(api_v1.url_for(Login), data=str(data),
                                    content_type='application/json')
        response_dict = eval(response.data.decode('UTF-8'))
        access_token = response_dict.get('access_token', None)
        return access_token

    def get_requests(self, logged_in: bool = True, admin=False,
                     admin_views_all: bool = False):
        """
        Helper function for making a request via the server.
        :param admin_views_all: Whether or not admin will be used to view other
        user's request
        :param admin: What user role should be used
        :param logged_in: Whether a user should be logged in or not
        :return: response object
        """

        if admin:
            email = 'viewrequest@admin.com'
        else:
            email = 'viewrequest@consumer.com'

        if admin_views_all:
            email = 'viewrequest@admin.com'

        access_token = self.login(dict(email=email,
                                       password='password.Pa55word'))

        try:
            Request(
                dict(
                    user_id=
                    db.get_user_by_email('editrequets@consumer.com')[
                        'user_id'],
                    email='editrequets@consumer.com',
                    role='Consumer'),
                'Repair', 'My Request Title', 'An explanation of what happened '
                                              'to justify this request.'
            )
        except RequestTransactionError:
            pass

        if admin_views_all:
            email = 'viewrequests@consumer.com'
        request_id = 1
        if logged_in:
            return self.client.get(api_v1.url_for(SingleUserSingleRequest,
                                                  request_id=request_id),
                                   content_type='application/json',
                                   headers={
                                       'ACCESS_TOKEN':
                                           access_token})
        else:
            return self.client.get(api_v1.url_for(SingleUserSingleRequest,
                                                  request_id=request_id),
                                   content_type='application/json')

    def test_get_my_request_requires_login(self):
        """
        Test that this route requires login
        :return:
        """
        response = self.get_requests(False)
        self.assert401(response)

    def test_get_my_request_consumer_pass(self):
        """
        Test that a consumer can view their requests
        :return:
        """
        response = self.get_requests()
        self.assertIn(b'request', response.data)
        self.assert200(response)

    def test_get_my_request_admin_fail(self):
        """
        Test that Administrators do not have requests
        :return:
        """
        response = self.get_requests(admin=True)
        self.assertIn(b'Administrators do not have requests', response.data)
