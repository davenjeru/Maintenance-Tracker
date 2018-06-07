import unittest

from MaintenanceTrackerAPI._tests import db
from MaintenanceTrackerAPI.api.v1.exceptions import RequestTransactionError
from MaintenanceTrackerAPI.api.v1.models.request_model import Request
from MaintenanceTrackerAPI.api.v1.models.user_model import User

# clear the database
db.drop_all()
db.create_all()

# save a user in the database
u = User('email@company.com', 'password.Pa55word',
         'What is your favourite company?', 'company')


class RequestBaseTestCase(unittest.TestCase):
    def setUp(self):
        """
        Overridden method from unittest.TestCase class

        :return: None
        """
        self.user_dict = dict(email='email@company.com',
                              user_id=1,
                              role='Consumer')
        self.arguments = dict(user=self.user_dict,
                              request_type='Repair',
                              title='Laptop Repair',
                              description='Water spilled onto my keyboard.'
                                          ' I need it replaced')

    def tearDown(self):
        """
        Overridden method from unittest.TestCase class

        :return: None
        """
        pass

    def expect_request_transaction_error(self, expected_error_message: str,
                                         the_callable: callable,
                                         arguments: dict):
        """
        This function helps refactor how to assert that an exception is raised
        :param expected_error_message: The expected error message
        :param the_callable: The function that is supposed to raise that error
         given the arguments
        :param arguments: arguments to use when calling the callable
        :return:
        """
        with self.assertRaises(RequestTransactionError) as a:
            the_callable(arguments['user'],
                         arguments['request_type'],
                         arguments['title'], arguments['description'])
        exception = a.exception
        self.assertEqual(expected_error_message, exception.msg)


class MakeRequestTestCase(RequestBaseTestCase):

    def test_consumer_makes_request(self):
        """
        Test that consumer can make requests
        :return: None
        """
        request = Request(self.user_dict, 'Repair', 'Laptop Repair',
                          'Water spilled onto my keyboard. I need it replaced')
        self.assertEqual(request.user_id, self.user_dict['user_id'])
        self.assertEqual(request.status, 'Pending Approval')

    def test_admin_makes_request_fail(self):
        """
        Test that an Administrator cannot create a request.
        :return:
        """
        self.user_dict['role'] = 'Administrator'
        expected_error_message = 'Administrators cannot make requests!'
        self.expect_request_transaction_error(expected_error_message,
                                              Request, self.arguments)

    def test_make_request_with_invalid_title(self):
        """
        Test that request cannot be made with invalid title
        :return: None
        """
        self.arguments['title'] = '############'
        expected_error_message = 'please enter a valid title'
        self.expect_request_transaction_error(expected_error_message,
                                              Request, self.arguments)
        self.arguments['title'] = 'Help Me**~##'
        self.expect_request_transaction_error(expected_error_message,
                                              Request, self.arguments)

    def test_make_request_with_short_title(self):
        """
        Test that request cannot be made with a title that is too short
        :return: None
        """
        self.arguments['title'] = 'XX'
        expected_error_message = 'title too short. Min of 10 characters allowed'
        self.expect_request_transaction_error(expected_error_message, Request,
                                              self.arguments)

    def test_make_request_with_long_title(self):
        """
        Test that request cannot be made with a title that is too long
        :return: None
        """
        self.arguments['title'] = 'Dokokara mitemo itsumademo syle mo' \
                                  ' ginsei sutekidayo ishoukillin it fuan'
        expected_error_message = 'title too long. Max of 70 characters allowed'
        self.expect_request_transaction_error(expected_error_message, Request,
                                              self.arguments)

    def test_make_request_with_wrong_spacing_title(self):
        """
        Test that request cannot be made with a title that has wrong spacing
        :return: None
        """
        self.arguments['title'] = 'X                     X'
        expected_error_message = 'Please check the spacing on your title'
        self.expect_request_transaction_error(expected_error_message, Request,
                                              self.arguments)

    def test_make_request_with_wrong_punctuation_title(self):
        """
        Test that request cannot be made with a title that has wrong punctuation
        :return: None
        """
        self.arguments['title'] = 'Aka..\'.\';.\'.;\'.'
        expected_error_message = 'please check the punctuation in your title'
        self.expect_request_transaction_error(expected_error_message, Request,
                                              self.arguments)
        self.arguments['title'] = 'Just a title but....'
        self.expect_request_transaction_error(expected_error_message, Request,
                                              self.arguments)

    def test_make_request_with_invalid_description(self):
        """
        Test that request cannot be made with invalid description
        :return: None
        """
        self.arguments['description'] = '#######################' \
                                        '####################'
        expected_error_message = 'please enter a valid description'
        self.expect_request_transaction_error(expected_error_message, Request,
                                              self.arguments)

    def test_make_request_with_short_description(self):
        """
        Test that request cannot be made with a description that is too short
        :return: None
        """
        self.arguments['description'] = 'A'
        expected_error_message = 'description too short.' \
                                 ' Min of 40 characters allowed'
        self.expect_request_transaction_error(expected_error_message, Request,
                                              self.arguments)

    def test_make_request_with_long_description(self):
        """
        Test that request cannot be made with a description that is too long
        :return: None
        """
        self.arguments['description'] = """Water spilled onto my keyboard.
        I need it replaced. Water spilled onto my keyboard. I need it replaced.
        Water spilled onto my keyboard. I need it replaced. Water spilled onto
        my keyboard. I need it replaced. Water spilled onto my keyboard.
        I need it replaced. Water spilled onto my keyboard. I need it replaced
        """
        expected_error_message = 'description too long.' \
                                 ' Max of 250 characters allowed'
        self.expect_request_transaction_error(expected_error_message, Request,
                                              self.arguments)

    def test_make_request_with_wrong_spacing_description(self):
        """
        Test that request cannot be made with wrong spacing in the description
        :return: None
        """
        self.arguments['description'] = """W          lled onto my keyboard.
              I need it             replaced"""
        expected_error_message = 'Please check the spacing on your description'
        self.expect_request_transaction_error(expected_error_message, Request,
                                              self.arguments)

    def test_make_request_with_wrong_punctuation_description(self):
        """
        Test that request cannot be made with wrong punctuation
         in the description
        :return: None
        """
        self.arguments['description'] = """Water spilled onto my Aka..\'.\'.;\'.
         I need it reAka..\'.\';.\'.;\'.placed"""
        expected_error_message = \
            'please check the punctuation in your description'
        self.expect_request_transaction_error(expected_error_message, Request,
                                              self.arguments)

    def test_make_request_twice(self):
        """
        Test that a request cannot be made more than once
        :return: None
        """
        expected_error_message = 'similar request exists'
        self.expect_request_transaction_error(expected_error_message, Request,
                                              self.arguments)
