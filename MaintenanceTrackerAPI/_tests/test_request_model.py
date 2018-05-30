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
