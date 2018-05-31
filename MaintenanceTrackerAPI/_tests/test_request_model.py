import unittest

from MaintenanceTrackerAPI.api.v1.models.request_model import Request, RequestTransactionError, requests_list
from MaintenanceTrackerAPI.api.v1.models.user_model import Consumer, Admin, users_list


class BaseRequestTestCase(unittest.TestCase):

    def setUp(self):
        users_list.clear()
        requests_list.clear()
        self.consumer = Consumer('consumer@company.com', 'password.Pa55word', 'What is your favourite company?',
                                 'company')
        self.admin = Admin('admin@company.com', 'password.Pa55word', 'What is your favourite company?',
                           'company')
        self.arguments = dict(user=self.consumer, request_type='Maintenance', title='Laptop Maintenance',
                              description='Keyboard cleaning and heat shield replacement')

        self.request = Request(self.consumer, 'Maintenance', 'Laptop Maintenance',
                               'Keyboard cleaning and heat shield replacement')

    def expect_request_transaction_error(self, expected_error_message: str, the_callable: callable, arguments: dict):
        """
        This function helps refactor how to assert that an exception is raised
        :param expected_error_message: The expected error message
        :param the_callable: The function that is supposed to raise that error given the arguments
        :param arguments: arguments to use when calling the callable
        :return:
        """
        with self.assertRaises(RequestTransactionError) as a:
            the_callable(arguments['user'], arguments['request_type'], arguments['title'], arguments['description'])
        exception = a.exception
        self.assertEqual(expected_error_message, exception.msg)


class MakeRequestTestCase(BaseRequestTestCase):

    def test_consumer_makes_request(self):
        request = Request(self.consumer, 'Repair', 'Laptop Repair',
                          'Water spilled onto my keyboard. I need it replaced')
        self.assertEqual(request.user_id, self.consumer.id)

    def test_admin_makes_request_fail(self):
        self.arguments['user'] = self.admin
        expected_error_message = 'Administrators cannot make requests!'
        self.expect_request_transaction_error(expected_error_message, Request, self.arguments)

    def test_make_request_with_invalid_title(self):
        self.arguments['title'] = '############'
        expected_error_message = 'please enter a valid title'
        self.expect_request_transaction_error(expected_error_message, Request, self.arguments)

    def test_make_request_with_short_title(self):
        self.arguments['title'] = 'XX'
        expected_error_message = 'title too short. Min of 10 characters allowed'
        self.expect_request_transaction_error(expected_error_message, Request, self.arguments)

    def test_make_request_with_long_title(self):
        self.arguments['title'] = 'Dokokara mitemo itsumademo syle mo ginsei sutekidayo ishoukillin it fuan'
        expected_error_message = 'title too long. Max of 70 characters allowed'
        self.expect_request_transaction_error(expected_error_message, Request, self.arguments)

    def test_make_request_with_wrong_spacing_title(self):
        self.arguments['title'] = 'X                     X'
        expected_error_message = 'Please check the spacing on your title'
        self.expect_request_transaction_error(expected_error_message, Request, self.arguments)

    def test_make_request_with_wrong_punctuation_title(self):
        self.arguments['title'] = 'Aka..\'.\';.\'.;\'.'
        expected_error_message = 'please check the punctuation in your title'
        self.expect_request_transaction_error(expected_error_message, Request, self.arguments)

    def test_make_request_with_invalid_description(self):
        self.arguments['description'] = '###########################################'
        expected_error_message = 'please enter a valid description'
        self.expect_request_transaction_error(expected_error_message, Request, self.arguments)

    def test_make_request_with_short_description(self):
        self.arguments['description'] = 'A'
        expected_error_message = 'description too short. Min of 40 characters allowed'
        self.expect_request_transaction_error(expected_error_message, Request, self.arguments)

    def test_make_request_with_long_description(self):
        self.arguments['description'] = """Water spilled onto my keyboard. I need it replaced. Water spilled onto my 
        keyboard. I need it replaced. Water spilled onto my keyboard. I need it replaced. Water spilled onto my 
        keyboard. I need it replaced. Water spilled onto my keyboard. I need it replaced. Water spilled onto my 
        keyboard. I need it replaced """
        expected_error_message = 'description too long. Max of 250 characters allowed'
        self.expect_request_transaction_error(expected_error_message, Request, self.arguments)

    def test_make_request_with_wrong_spacing_description(self):
        self.arguments['description'] = 'W               lled onto my keyboard.      I need it replaced'
        expected_error_message = 'Please check the spacing on your description'
        self.expect_request_transaction_error(expected_error_message, Request, self.arguments)

    def test_make_request_with_wrong_punctuation_description(self):
        self.arguments['description'] = 'Water spilled onto my Aka..\'.\'.;\'. I need it reAka..\'.\';.\'.;\'.placed'
        expected_error_message = 'please check the punctuation in your description'
        self.expect_request_transaction_error(expected_error_message, Request, self.arguments)

    def test_make_request_twice(self):
        expected_error_message = 'similar request exists'
        self.expect_request_transaction_error(expected_error_message, Request, self.arguments)


class RespondRequestTestCase(BaseRequestTestCase):

    def test_admin_approves_request(self):
        self.request.approve(self.admin)
        self.assertEqual('Approved', self.request.status)

    def test_admin_rejects_request(self):
        self.request.reject(self.admin)
        self.assertEqual('Rejected', self.request.status)

    def test_admin_marks_request_in_progress(self):
        self.request.approve(self.admin)
        self.request.in_progress(self.admin)
        self.assertEqual('In Progress', self.request.status)

    def test_admin_resolves_request(self):
        self.request.approve(self.admin)
        self.request.in_progress(self.admin)
        self.request.resolve(self.admin)
        self.assertEqual('Resolved', self.request.status)

    def test_consumer_approves_request_fail(self):
        with self.assertRaises(RequestTransactionError) as a:
            self.request.approve(self.consumer)
        exception = a.exception
        self.assertEqual('Consumer not allowed to change request status', exception.msg)

    def test_consumer_rejects_request_fail(self):
        with self.assertRaises(RequestTransactionError) as a:
            self.request.reject(self.consumer)
        exception = a.exception
        self.assertEqual('Consumer not allowed to change request status', exception.msg)

    def test_consumer_marks_request_in_progress_fail(self):
        with self.assertRaises(RequestTransactionError) as a:
            self.request.in_progress(self.consumer)
        exception = a.exception
        self.assertEqual('Consumer not allowed to change request status', exception.msg)

    def test_consumer_resolves_request_fail(self):
        with self.assertRaises(RequestTransactionError) as a:
            self.request.resolve(self.consumer)
        exception = a.exception
        self.assertEqual('Consumer not allowed to change request status', exception.msg)

    def test_consumer_cancels_request(self):
        self.request.cancel(self.consumer)
        self.assertEqual('Cancelled', self.request.status)

    def test_consumer_deletes_request(self):
        self.request.cancel(self.consumer)
        self.request.delete(self.consumer)
        self.assertNotIn(self.request, requests_list)

    def test_admin_cancels_request_fail(self):
        with self.assertRaises(RequestTransactionError) as a:
            self.request.cancel(self.admin)
        exception = a.exception
        self.assertEqual('Administrator not allowed to cancel request', exception.msg)

    def test_admin_deletes_request_fail(self):
        with self.assertRaises(RequestTransactionError) as a:
            self.request.delete(self.admin)
        exception = a.exception
        self.assertEqual('Administrator not allowed to delete request', exception.msg)


class EditRequestTestCase(BaseRequestTestCase):

    def test_consumer_edits_request(self):
        self.request.edit(self.consumer,
                          dict(title='Another Title',
                               description='Another description for testing and must reach forty characters'))
        self.assertEqual(self.request.title, 'Another Title')

    def test_admin_edits_request_fail(self):
        with self.assertRaises(RequestTransactionError) as a:
            self.request.edit(self.admin,
                              dict(title='Another Title',
                                   description='Another description for testing and must reach forty characters'))
        exception = a.exception
        self.assertEqual('Administrator not allowed to edit request', exception.msg)

    def test_consumer_edits_cancelled_request_fail(self):
        self.request.cancel(self.consumer)
        with self.assertRaises(RequestTransactionError) as a:
            self.request.edit(self.consumer,
                              dict(title='Another Title',
                                   description='Another description for testing and must reach forty characters'))
        exception = a.exception
        self.assertEqual('cannot edit a request which is Cancelled', exception.msg)
