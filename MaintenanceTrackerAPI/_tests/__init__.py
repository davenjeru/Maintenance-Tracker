from flask_testing import TestCase

from MaintenanceTrackerAPI import create_app as create
from MaintenanceTrackerAPI.api.v1 import api_v1
from MaintenanceTrackerAPI.api.v1.auth import Register
from MaintenanceTrackerAPI.api.v1.database import Database

db = Database()


class BaseTestCase(TestCase):
    def create_app(self):
        """
        Create the Flask application with 'testing' as the configuration
        :return: app -> the Flask app
        """
        app = create('testing')
        return app

    def setUp(self):
        self.client = self.create_app().test_client()

    def test_no_base_url(self):
        """
        Test the root index '/' of the app
        This test fails if there was something wrong with creating the Flask app
        :return: None
        """
        response = self.client.get('/')
        self.assert404(response)

    def test_api_index(self):
        """
        Test the base url of the api(v1) '/api/v1/'
        This test fails if the Api Blueprint was not registered by the Flask app
        :return: None
        """
        response = self.client.get(api_v1.base_url)
        self.assert200(response)

    def test_not_json(self):
        """
        Test when the request lacks header lacks
         'content_type='application/json''
        :return: None
        """
        response = self.client.post(api_v1.url_for(Register))
        self.assertEqual(415, response.status_code)

    def test_no_data(self):
        """
        Test that the server checks when the request body is empty
        :return: None
        """
        response = self.client.post(api_v1.url_for(Register),
                                    content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertIn(b'no data was found in the request', response.data)
