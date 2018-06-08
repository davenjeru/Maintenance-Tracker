import unittest

from MaintenanceTrackerAPI._tests import db
from MaintenanceTrackerAPI.api.v1.exceptions import UserTransactionError
from MaintenanceTrackerAPI.api.v1.models.user_model import User

# clear the database
db.drop_all()
db.create_all()

# save a user in the database
u = User('createuser@company.com', 'password.Pa55word',
         'What is your favourite company?', 'company')


class UserBaseTestCase(unittest.TestCase):
    def setUp(self):
        """
        Overridden method from unittest.TestCase class

        :return: None
        """
        self.arguments = dict(email='createuser@company.com',
                              password='password.Pa55word',
                              security_question='What'
                                                ' is your favourite company?',
                              security_answer='company')

    def tearDown(self):
        """
        Overridden method from unittest.TestCase class

        :return: None
        """
        pass

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


class CreateUserTestCase(UserBaseTestCase):

    def test_create_user_pass(self):
        """
        Test that a user can be created
        :return: None
        """
        self.assertEqual('createuser@company.com', u.email)

    def test_create_duplicate_user(self):
        """
        Test that a user cannot be created with an email similar to one in the
        database
        :return: None
        """
        try:
            User('createuser@company.com', 'password.Pa55word',
                 'What is your favourite company?', 'company')
        except UserTransactionError:
            pass
        expected_error_message = 'user with similar email exists'
        self.expect_user_transaction_error(expected_error_message,
                                           User, self.arguments)

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
        self.arguments['security_question'] = 'Where are you.'
        expected_error_message = 'security question must end with a' \
                                 ' question mark \'?\''
        self.expect_user_transaction_error(expected_error_message,
                                           User, self.arguments)
        self.arguments['security_question'] = 'Where .,.,.,, .,are you?'
        expected_error_message = 'security question must not contain any' \
                                 ' punctuations mid sentence'
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
        self.arguments['security_answer'] = 'm    b     bbs'
        expected_error_message = 'Please check the spacing on' \
                                 ' your security answer'
        self.expect_user_transaction_error(expected_error_message,
                                           User, self.arguments)
        self.arguments['security_answer'] = 'Answeriolkdijrhtbfjsppoiewsasw'
        expected_error_message = 'security answer too long.' \
                                 ' Max of 20 characters'
        self.expect_user_transaction_error(expected_error_message,
                                           User, self.arguments)
        self.arguments['security_answer'] = 'n'
        expected_error_message = 'security answer is too short.' \
                                 ' Min of 5 characters'
        self.expect_user_transaction_error(expected_error_message,
                                           User, self.arguments)

    def test_create_user_missing_params(self):
        """
        Test that a user cannot be created with missing params
        :return: None
        """
        self.arguments['security_answer'] = ''
        expected_error_message = 'missing "security answer" parameter'
        self.expect_user_transaction_error(expected_error_message,
                                           User, self.arguments)

    def test_create_admin_user_pass(self):
        """
        Test that an Administrator can be created
        :return: None
        """
        admin = User('admin@company.com', 'password.Pa55word',
                     'What is your favourite company?', 'company',
                     'Administrator')
        self.assertEqual('Administrator', admin.role)

    def test_create_consumer_user_pass(self):
        """
        Test that a Consumer can be created
        :return: None
        """
        consumer = User('consumer1@company.com', 'password.Pa55word',
                        'What is your favourite company?', 'company')
        self.assertEqual('Consumer', consumer.role)
