from flask_testing import TestCase

from MaintenanceTrackerAPI import create_app as create


class AppTestCase(TestCase):
    def create_app(self):
        app = create('testing')
        return app

    def setUp(self):
        self.client = self.create_app().test_client()

    def tearDown(self):
        pass

    def test_no_base_index(self):
        response = self.client.get('/')
        self.assert404(response)

    def test_api_index(self):
        response = self.client.get(api_v1.base_url)
        self.assert200(response)

    def test_not_json(self):
        response = self.client.post(api_v1.url_for(Register))
        self.assertEqual(415, response.status_code)

    def test_no_data(self):
        response = self.client.post(api_v1.url_for(Register), content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertIn(b'no data was found in the request', response.data)

    def register(self, email: str = None, password_tuple: tuple = (None, None), security_tuple: tuple = (None, None)):
        data = dict(email=email)
        data['password'], data['confirm_password'] = password_tuple
        data['security_question'], data['security_answer'] = security_tuple
        return self.client.post(api_v1.url_for(Register), data=str(data), content_type='application/json')

    def test_a1_consumer_register_pass(self):
        password_tuple = ('password.Pa55word', 'password.Pa55word')
        security_tuple = ('What is your favourite company?', 'company')

        response = self.register('consumer@company.com', password_tuple, security_tuple)
        self.assertEqual(201, response.status_code)
        self.assertEqual(b'Consumer', response.data)
        self.assertIn(b'user registered successfully', response.data)
        response = self.register('consumer@company.com', password_tuple, security_tuple)
        self.assertIn(b'user with similar email exists', response.data)
        self.assert400(response)

    def test_a1_admin_register_pass(self):
        password_tuple = ('password.Pa55word', 'password.Pa55word')
        security_tuple = ('What is your favourite company?', 'company')

        response = self.register('admin@company.com', password_tuple, security_tuple)
        self.assertEqual(201, response.status_code)
        self.assertEqual(b'Consumer', response.data)
        self.assertIn(b'user registered successfully', response.data)
        response = self.register('admin@company.com', password_tuple, security_tuple)
        self.assertIn(b'user with similar email exists', response.data)
        self.assert400(response)

    def test_a2_register_missing_parameter(self):
        response = self.register('email@company.com')
        self.assert400(response)
        self.assertIn(b'missing', response.data)

    def test_a3_register_invalid_password(self):
        password_tuple = ('password', 'password')
        security_tuple = ('What is your favourite company?', 'company')
        response = self.register('email@company.com', password_tuple, security_tuple)
        self.assert400(response)
        self.assertIn(b'password syntax is invalid', response.data)

    def test_a4_register_passwords_no_match(self):
        password_tuple = ('password.Pa55word', 'password')
        security_tuple = ('What is your favourite company?', 'company')
        response = self.register('email@company.com', password_tuple, security_tuple)
        self.assert400(response)
        self.assertIn(b'passwords do not match', response.data)

    def login(self, email: str = None, password: str = None):
        data = dict(email=email, password=password)
        return self.client.post(api_v1.url_for(Login), data=str(data), content_type='application/json')

    def test_a7_login(self):
        email = 'consumer@company.com'
        password = 'password.Pa55word'
        response = self.login(email, password)
        self.assert200(response)
        self.assertIn(b'user logged in successfully', response.data)

        response = self.login(email, password)
        self.assert400(response)
        self.assertIn(b'currently logged in', response.data)

    def test_a8_login_fail(self):
        email = 'consumer@company.com'
        password = 'not.a.5imilaRpass'
        response = self.login(email, password)
        self.assert401(response)
        self.assertIn(b'invalid password', response.data)

        email = 'email254@company.com'
        response = self.login(email, password)
        self.assert400(response)
        self.assertIn(b'user not found', response.data)

        response = self.login(None, password)
        self.assert400(response)
        self.assertIn(b'missing', response.data)

    def test_a9_logout(self):
        self.login('consumer@company.com', 'password.Pa55word')
        response = self.client.post(api_v1.url_for(Logout))
        self.assert200(response)
        self.assertIn(b'logged out successfully', response.data)
        response = self.client.post(api_v1.url_for(Logout))
        self.assert400(response)
        self.assertIn(b'no user in session', response.data)
