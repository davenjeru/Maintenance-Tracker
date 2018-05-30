import unittest

from MaintenanceTrackerAPI.api.v1.models.request_model import Request, RequestTransactionError, requests_list
from MaintenanceTrackerAPI.api.v1.models.user_model import Consumer, Admin, users_list


class RequestTestCase(unittest.TestCase):

    def setUp(self):
        users_list.clear()
        requests_list.clear()
        self.consumer = Consumer('consumer@company.com', 'password.Pa55word', 'What is your favourite company?',
                                 'company')
        self.admin = Admin('admin@company.com', 'password.Pa55word', 'What is your favourite company?',
                           'company')

    def test_consumer_makes_request(self):
        request = Request(self.consumer, 'Repair', 'Laptop Repair',
                          'Water spilled onto my keyboard. I need it replaced')
        self.assertEqual(request.user_id, self.consumer.id)

    def test_admin_makes_request_fail(self):
        with self.assertRaises(RequestTransactionError) as a:
            Request(self.admin, 'Repair', 'Laptop Repair',
                    'Water spilled onto my keyboard. I need it replaced')
        exception = a.exception
        self.assertEqual('Administrators cannot make requests!', exception.msg)

    def test_make_request_with_invalid_title(self):
        with self.assertRaises(RequestTransactionError) as a:
            Request(self.consumer, 'Repair', '############',
                    'Water spilled onto my keyboard. I need it replaced')
        exception = a.exception
        self.assertEqual('please enter a valid title', exception.msg)

    def test_make_request_with_short_title(self):
        with self.assertRaises(RequestTransactionError) as a:
            Request(self.consumer, 'Repair', 'XX',
                    'Water spilled onto my keyboard. I need it replaced')
        exception = a.exception
        self.assertEqual('title too short. Min of 10 characters allowed', exception.msg)

    def test_make_request_with_long_title(self):
        with self.assertRaises(RequestTransactionError) as a:
            Request(self.consumer, 'Repair', 'Dokokara mitemo itsumademo syle mo ginsei sutekidayo ishoukillin it fuan',
                    'Water spilled onto my keyboard. I need it replaced')
        exception = a.exception
        self.assertEqual('title too long. Max of 70 characters allowed', exception.msg)

    def test_make_request_with_wrong_spacing_title(self):
        with self.assertRaises(RequestTransactionError) as a:
            Request(self.consumer, 'Repair', 'X                     X',
                    'Water spilled onto my keyboard. I need it replaced')
        exception = a.exception
        self.assertEqual('Please check the spacing on your title', exception.msg)

    def test_make_request_with_wrong_punctuation_title(self):
        with self.assertRaises(RequestTransactionError) as a:
            Request(self.consumer, 'Repair', 'Aka..\'.\';.\'.;\'.',
                    'Water spilled onto my keyboard. I need it replaced')
        exception = a.exception
        self.assertEqual('please check the punctuation in your title', exception.msg)

    def test_make_request_with_invalid_description(self):
        with self.assertRaises(RequestTransactionError) as a:
            Request(self.consumer, 'Repair', 'Laptop Repair',
                    '###########################################')
        exception = a.exception
        self.assertEqual('please enter a valid description', exception.msg)

    def test_make_request_with_short_description(self):
        with self.assertRaises(RequestTransactionError) as a:
            Request(self.consumer, 'Repair', 'Laptop Repair',
                    'W')
        exception = a.exception
        self.assertEqual('description too short. Min of 40 characters allowed', exception.msg)

    def test_make_request_with_long_description(self):
        with self.assertRaises(RequestTransactionError) as a:
            Request(self.consumer, 'Repair', 'Laptop Repair',
                    'Water spilled onto my keyboard. I need it replacedWatspilled onto my keyboard. I need it replace'
                    'Water spilled onto my keyboard. I need it replacedWater sped onto my keyboard. I need it replaced'
                    'Water spilled onto my keyboard. I need it replacedWater spilled onto my keyboard. I need it replac'
                    'Water spilled onto my keyboard. I need it replacedWater spilled onto my keyboard. I need it replac'
                    'Water spilled onto my keyboard. I need it replaced')
        exception = a.exception
        self.assertEqual('description too long. Max of 250 characters allowed', exception.msg)

    def test_make_request_with_wrong_spacing_description(self):
        with self.assertRaises(RequestTransactionError) as a:
            Request(self.consumer, 'Repair', 'Laptop Repair',
                    'W               lled onto my keyboard.      I need it replaced')
        exception = a.exception
        self.assertEqual('Please check the spacing on your description', exception.msg)

    def test_make_request_with_wrong_punctuation_description(self):
        with self.assertRaises(RequestTransactionError) as a:
            Request(self.consumer, 'Repair', 'Laptop Repair',
                    'Water spilled onto my Aka..\'.\';.\'.;\'. I need it reAka..\'.\';.\'.;\'.placed')
        exception = a.exception
        self.assertEqual('please check the punctuation in your description', exception.msg)

    def test_make_request_twice(self):
        Request(self.consumer, 'Repair', 'Laptop Repair',
                'Water spilled onto my keyboard. I need it replaced')
        with self.assertRaises(RequestTransactionError) as a:
            Request(self.consumer, 'Repair', 'Laptop Repair',
                    'Water spilled onto my keyboard. I need it replaced')
            exception = a.exception
            self.assertEqual('similar request exists', exception.msg)
