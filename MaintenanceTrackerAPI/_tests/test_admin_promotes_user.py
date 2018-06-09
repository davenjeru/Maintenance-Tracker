from MaintenanceTrackerAPI._tests import BaseTestCase, db
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.auth import Login
from MaintenanceTrackerAPI.api.v1.exceptions import UserTransactionError
from MaintenanceTrackerAPI.api.v1.models.user_model import User
from MaintenanceTrackerAPI.api.v1.users import SingleUserAction


class PromoteUserTestCase(BaseTestCase):
    db.drop_all()
    db.create_all()

    def login(self, data: dict):
        """
        Helper function for logging in a user.
        :param data: A dictionary containing data necessary for logging in
        :return: response object
        """
        try:
            User('adminpromotesuser@consumer.com', 'password.Pa55word',
                 'What is your favourite company?', 'Company')
            User('adminpromotesuser@admin.com', 'password.Pa55word',
                 'What is your favourite company?', 'Company',
                 'Administrator')
        except UserTransactionError:
            pass

        response = self.client.post(api_v1.url_for(Login), data=str(data),
                                    content_type='application/json')
        response_dict = eval(response.data.decode('UTF-8'))
        access_token = response_dict.get('access_token', None)
        return access_token

    def promote_or_demote_user(self, action: str, logged_in: bool = True,
                               admin=True, consumer: bool = True):
        """
        Helper function for making a request via the server.
        :param admin: What user role should be used
        :param logged_in: Whether a user should be logged in or not
        :return: response object
        """
        user_id = 1
        if not logged_in:
            return self.client.put(api_v1.url_for(SingleUserAction,
                                                  user_id=user_id,
                                                  action=action),
                                   content_type='application/json')
        if admin:
            # email is equal to admin
            email = 'adminpromotesuser@admin.com'
        else:
            # email is equal to consumer
            email = 'adminpromotesuser@consumer.com'
        # login the performer
        access_token = self.login(dict(email=email,
                                       password='password.Pa55word'))

        if consumer:
            user_id = db.get_user_by_email('adminpromotesuser@'
                                           'consumer.com')['user_id']
        else:
            user_id = db.get_user_by_email('adminpromotesuser@'
                                           'admin.com')['user_id']
        return self.client.put(api_v1.url_for(SingleUserAction,
                                              user_id=user_id,
                                              action=action),
                               content_type='application/json',
                               headers={
                                   'ACCESS_TOKEN':
                                       access_token})

    def test_admin_promote_user_requires_login(self):
        """
        Test that this route requires login
        :return:
        """
        response = self.promote_or_demote_user('promote', logged_in=False)
        self.assert401(response)

    def test_admin_promotes_and_demotes_user_pass(self):
        """
        Test that a consumer can view their requests
        :return:
        """
        response = self.promote_or_demote_user('promote')
        self.assertIn(b'promoted', response.data)
        self.assert200(response)

        response = self.promote_or_demote_user('demote')
        self.assertIn(b'demoted', response.data)
        self.assert200(response)

    def test_consumer_promotes_user_fail(self):
        """
        Test that Administrators do not have requests
        :return:
        """
        response = self.promote_or_demote_user('promote', admin=False)
        self.assert403(response)

    def test_admin_promotes_admin(self):
        response = self.promote_or_demote_user('promote', consumer=False)
        self.assertIn(b'cannot', response.data)
