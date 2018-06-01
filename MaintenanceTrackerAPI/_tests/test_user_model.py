import unittest

from MaintenanceTrackerAPI.api.v1.models.user_model import User, \
    UserTransactionError, users_list, Admin, Consumer


class UserBaseTestCase(unittest.TestCase):
    def setUp(self):
        """
        Overridden method from unittest.TestCase class

        :return: None
        """
        users_list.clear()
        self.arguments = dict(email='email@company.com',
                              password='password.Pa55word',
                              security_question='What'
                                                ' is your favourite company?',
                              security_answer='company')

        self.u = User('email@company.com', 'password.Pa55word',
                      'What is your favourite company?', 'company')

    def tearDown(self):
        """
        Overridden method from unittest.TestCase class

        :return: None
        """
        users_list.clear()

    def expect_user_transaction_error(self, expected_error_message: str,
                                      the_callable: callable, arguments: dict):
        """
        This function helps refactor how to assert that an exception is raised
        :param expected_error_message: The expected error message
        :param the_callable: The function that is supposed to raise that error
         given the arguments
        :param arguments: arguments to use when calling the callable
        :return:
        """
        with self.assertRaises(UserTransactionError) as a:
            the_callable(arguments['email'], arguments['password'],
                         arguments['security_question'],
                         arguments['security_answer'])
        exception = a.exception
        self.assertEqual(expected_error_message, exception.msg)


class ModelsTestCase(UserBaseTestCase):

    def test_create_user_pass(self):
        """
        Test that a user can be created
        :return: None
        """
        self.assertEqual('email@company.com', self.u.email)
        self.assertTrue(self.u.authenticate('password.Pa55word'))

    def test_create_user_with_wrong_email_syntax(self):
        """
        Test that a user cannot be created with invalid email value
        :return: None
        """
        # test user creation with wrong email syntax
        self.arguments['email'] = 'email@com'
        expected_error_message = 'email address syntax is invalid'
        self.expect_user_transaction_error(expected_error_message,
                                           User, self.arguments)

    def test_create_user_with_wrong_password_syntax(self):
        """
        Test that a user cannot be created with invalid password syntax
        :return: None
        """
        # test user creation with wrong password syntax
        self.arguments['password'] = 'password'
        expected_error_message = 'password syntax is invalid'
        self.expect_user_transaction_error(expected_error_message,
                                           User, self.arguments)

    def test_create_user_with_wrong_security_question_syntax(self):
        """
        Test that a user cannot be created with wrong security question syntax
        :return: None
        """
        # test user creation with wrong security question syntax
        self.arguments['security_question'] = 'question'
        expected_error_message = 'security question must start' \
                                 ' with a \'Wh\' or a \'Are\' question'
        self.expect_user_transaction_error(expected_error_message,
                                           User, self.arguments)

    def test_create_user_with_wrong_security_answer_syntax(self):
        """
        Test that a user cannot be created with wrong security answer syntax
        :return: None
        """
        # test user creation with wrong security answer syntax
        self.arguments['security_answer'] = 'smm.vf....ff.,'
        expected_error_message = 'security answer must not' \
                                 ' contain any punctuations'
        self.expect_user_transaction_error(expected_error_message,
                                           User, self.arguments)

    def test_user_reset_password_pass(self):
        """
        Test that a user can reset their password
        :return: None
        """
        self.u.reset_password('What is your favourite company?',
                              'company', 'another.Pa55word')
        self.assertTrue(self.u.authenticate('another.Pa55word'))

    def test_user_reset_password_with_wrong_security_question(self):
        """
        Test that user cannot reset password with wrong security question
        :return: None
        """
        # reset password with wrong security question
        with self.assertRaises(UserTransactionError) as a:
            self.u.reset_password('favourite company?',
                                  'company', 'another.Pa55word')
        exception = a.exception
        self.assertEqual('wrong security question!', exception.msg)

    def test_user_reset_password_with_wrong_security_answer(self):
        """
        Test that user cannot reset password with wrong security answer
        :return: None
        """
        # reset password with wrong security answer
        with self.assertRaises(UserTransactionError) as a:
            self.u.reset_password('What is your favourite company?',
                                  'no answer', 'another.Pa55word')
        exception = a.exception
        self.assertEqual('wrong security answer!', exception.msg)

    def test_create_admin_user_pass(self):
        """
        Test that an Administrator can be created
        :return: None
        """
        admin = Admin('admin@company.com', 'password.Pa55word',
                      'What is your favourite company?', 'company')
        self.assertEqual('Administrator', admin.role)

    def test_create_consumer_user_pass(self):
        """
        Test that a Consumer can be created
        :return: None
        """
        consumer = Consumer('consumer@company.com', 'password.Pa55word',
                            'What is your favourite company?', 'company')
        self.assertEqual('Consumer', consumer.role)
