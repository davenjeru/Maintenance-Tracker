from MaintenanceTrackerAPI._tests import BaseTestCase
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.auth import Logout, Login


class LogoutTestCase(BaseTestCase):

    def test_logout(self):
        """
        Test the logout route
        :return: None
        """
        data = dict(email='consumer@company.com',
                    password='password.Pa55word')
        response = self.client.post(api_v1.url_for(Login), data=str(data),
                                    content_type='application/json')
        response_dict = eval(response.data.decode('UTF-8'))
        access_token = response_dict['access_token']
        response = self.client.post(api_v1.url_for(Logout))
        self.assert401(response)
        self.assertIn(b'Missing ACCESS_TOKEN Header', response.data)
        response = self.client.post(api_v1.url_for(Logout),
                                    headers={'access_token': access_token})
        self.assertIn(b'logged out successfully', response.data)
        response = self.client.post(api_v1.url_for(Logout),
                                    headers={'access_token': access_token})
        self.assertIn(b'Token has been revoked', response.data)
