from MaintenanceTrackerAPI._tests import BaseTestCase, db
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.auth import Login
from MaintenanceTrackerAPI.api.v1.exceptions import UserTransactionError, \
    RequestTransactionError
from MaintenanceTrackerAPI.api.v1.models.request_model import Request
from MaintenanceTrackerAPI.api.v1.models.user_model import User
from MaintenanceTrackerAPI.api.v1.users import SingleUserSingleRequest


class EditRequestTestCase(BaseTestCase):

    def setUp(self):
        self.data = dict(request_type=None,
                         title=None,
                         description=None)

    def login(self, data: dict):
        """
        Helper function for logging in a user.
        :param data: A dictionary containing data necessary for logging in
        :return: access token
        :rtype str
        """
        try:
            User('editrequets@consumer.com', 'password.Pa55word',
                 'What is your favourite company?', 'Company')
            User('editrequets@admin.com', 'password.Pa55word',
                 'What is your favourite company?', 'Company',
                 'Administrator')
        except UserTransactionError:
            pass

        response = self.client.post(api_v1.url_for(Login), data=str(data),
                                    content_type='application/json')
        response_dict = eval(response.data.decode('UTF-8'))
        access_token = response_dict.get('access_token', None)
        return access_token

    def edit_request(self, data: dict, logged_in: bool = True, admin=False):
        """
        Helper function for editing a request.
        :param admin: Whether or not an Administrator should be used
        :param logged_in:
        :param data: A dictionary containing data necessary for editing the
        request
        :return: response object
        """

        if admin:
            email = 'editrequets@admin.com'
        else:
            email = 'editrequets@consumer.com'

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
                'Repair', 'My Editting Title',
                'An explanation of what happened '
                                              'to justify this request.'
            )
        except RequestTransactionError:
            pass

        request_id = 2
        if logged_in:
            return self.client.patch(api_v1.url_for(SingleUserSingleRequest,
                                                    request_id=request_id),
                                     data=str(data),
                                     content_type='application/json',
                                     headers={
                                         'ACCESS_TOKEN':
                                             access_token})
        else:
            return self.client.patch(api_v1.url_for(SingleUserSingleRequest,
                                                    request_id=request_id),
                                     data=str(data),
                                     content_type='application/json')

    def test_login_required(self):
        """
        Test that login is required to access this route
        :return: None
        """
        self.data['title'] = 'Some Really Random Request Title'
        response = self.edit_request(self.data, logged_in=False)
        self.assert401(response)

    def test_consumer_can_edit_request(self):
        """
        Test that a consumer can edit a request
        :return: None
        """
        # edit the request title
        self.data['title'] = 'New Request Title'
        response = self.edit_request(self.data)
        self.assertIn(b'New Request Title', response.data)

        # edit request description
        self.data['title'] = None
        self.data['description'] = 'This is the new description. I\'m' \
                                   ' just doing this so that I can reach' \
                                   ' the minimum description character limit'
        response = self.edit_request(self.data)
        self.assertIn(b'This is the new description.', response.data)

    def test_admin_cannot_edit(self):
        """
        Test that an Administrator cannot edit a request
        :return: None
        """
        # edit the request title
        self.data['title'] = 'New Request Title'
        response = self.edit_request(self.data, admin=True)
        self.assert403(response)

    def test_wrong_title(self):
        """
        Test that a request cannot be edited with wrong title syntax
        :return: None
        """
        # edit the request title
        self.data['title'] = 'N dkknc/.../....;;;'
        response = self.edit_request(self.data)
        self.assert400(response)

    def test_edit_request_with_nothing(self):
        """
        Test that a request cannot be edited with nothing in the request body
        :return: None
        """
        # login
        data = dict(email='consumer@company.com', password='password.Pa55word')
        self.login(data)

        # remove all keys and values in the dictionary
        data.clear()
        response = self.edit_request(data)
        self.assertIn(b'could not edit request, please insert'
                      b' title or description',
                      response.data)
