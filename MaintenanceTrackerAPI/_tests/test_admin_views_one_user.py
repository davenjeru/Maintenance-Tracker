from MaintenanceTrackerAPI._tests import BaseTestCase, db
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.auth import Login
from MaintenanceTrackerAPI.api.v1.exceptions import UserTransactionError
from MaintenanceTrackerAPI.api.v1.models.user_model import User
from MaintenanceTrackerAPI.api.v1.users import SingleUser


class ViewOneRequestTestCase(BaseTestCase):
    db.drop_all()
    db.create_all()

    def login(self, data: dict):
        """
        Helper function for logging in a user.
        :param data: A dictionary containing data necessary for logging in
        :return: access token
        :rtype str
        """
        try:
            User('adminviewsoneuser@consumer.com', 'password.Pa55word',
                 'What is your favourite company?', 'Company')
            User('adminviewsoneuser@admin.com', 'password.Pa55word',
                 'What is your favourite company?', 'Company',
                 'Administrator')
        except UserTransactionError:
            pass

        response = self.client.post(api_v1.url_for(Login), data=str(data),
                                    content_type='application/json')
        response_dict = eval(response.data.decode('UTF-8'))
        access_token = response_dict.get('access_token', None)
        return access_token

    def get_one_user(self, logged_in: bool = True, admin=False):
        """
        Helper function for making a request via the server.
        user's request
        :param admin: What user role should be used
        :param logged_in: Whether a user should be logged in or not
        :return: response object
        """

        if admin:
            email = 'adminviewsoneuser@admin.com'
        else:
            email = 'adminviewsoneuser@consumer.com'

        access_token = self.login(dict(email=email,
                                       password='password.Pa55word'))
        user_id = db.get_user_by_email(email)['user_id']
        if logged_in:
            return self.client.get(api_v1.url_for(SingleUser,
                                                  user_id=user_id),
                                   content_type='application/json',
                                   headers={
                                       'ACCESS_TOKEN':
                                           access_token})
        else:
            return self.client.get(api_v1.url_for(SingleUser,
                                                  user_id=user_id),
                                   content_type='application/json')

    def test_admin_get_one_user_requires_login(self):
        """
        Test that this route requires login
        :return:
        """
        response = self.get_one_user(False)
        self.assert401(response)

    def test_admin_gets_one_user_pass(self):
        """
        Test that a consumer can view their requests
        :return:
        """
        response = self.get_one_user(admin=True)
        self.assertIn(b'user', response.data)
        self.assert200(response)

    def test_consumer_gets_one_user_fail(self):
        """
        Test that Administrators do not have requests
        :return:
        """
        response = self.get_one_user()
        self.assert403(response)
