import unittest

from MaintenanceTrackerAPI.api.v1.models.user_model import User, UserTransactionError, users_list, Admin, Consumer


class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        users_list.clear()
        self.u = User('email@company.com', 'password.Pa55word', 'What is your favourite company?', 'company')

    def tearDown(self):
        users_list.clear()

    def test_create_user_pass(self):
        self.assertEqual('email@company.com', self.u.email)
        self.assertTrue(self.u.authenticate('password.Pa55word'))

    def test_create_user_with_wrong_email_syntax(self):
        # test user creation with wrong email syntax
        with self.assertRaises(UserTransactionError) as a:
            User('email@com', 'password.Pa55word', 'What is your favourite company?', 'company')
        exception = a.exception
        self.assertEqual('email address syntax is invalid', exception.msg)

    def test_create_user_with_wrong_password_syntax(self):
        # test user creation with wrong password syntax
        with self.assertRaises(UserTransactionError) as a:
            User('email@company.com', 'password', 'What is your favourite company?', 'company')
        exception = a.exception
        self.assertEqual('password syntax is invalid', exception.msg)

    def test_create_user_with_wrong_security_question_syntax(self):
        # test user creation with wrong security question syntax
        with self.assertRaises(UserTransactionError) as a:
            User('email@company.com', 'password.Pa55word', 'question', 'company')
        exception = a.exception
        self.assertEqual('security question must start with a \'Wh\' or a \'Are\' question', exception.msg)

    def test_create_user_with_wrong_security_answer_syntax(self):
        # test user creation with wrong security answer syntax
        with self.assertRaises(UserTransactionError) as a:
            User('email@company.com', 'password.Pa55word', 'What is your favourite company?', 'smm.vf....ff.,')
        exception = a.exception
        self.assertEqual('security answer must not contain any punctuations', exception.msg)

    def test_user_reset_password_pass(self):
        self.u.reset_password('What is your favourite company?', 'company', 'another.Pa55word')
        self.assertTrue(self.u.authenticate('another.Pa55word'))

    def test_user_reset_password_with_wrong_security_question(self):
        # reset password with wrong security question
        with self.assertRaises(UserTransactionError) as a:
            self.u.reset_password('favourite company?', 'company', 'another.Pa55word')
        exception = a.exception
        self.assertEqual('wrong security question!', exception.msg)

    def test_user_reset_password_with_wrong_security_answer(self):
        # reset password with wrong security answer
        with self.assertRaises(UserTransactionError) as a:
            self.u.reset_password('What is your favourite company?', 'no answer', 'another.Pa55word')
        exception = a.exception
        self.assertEqual('wrong security answer!', exception.msg)

    def test_create_admin_user_pass(self):
        admin = Admin('email@com', 'password.Pa55word', 'What is your favourite company?', 'company')
        self.assertEqual('Administrator', admin.role)

    def test_create_consumer_user_pass(self):
        consumer = Consumer('email@com', 'password.Pa55word', 'What is your favourite company?', 'company')
        self.assertEqual('Consumer', consumer.role)
