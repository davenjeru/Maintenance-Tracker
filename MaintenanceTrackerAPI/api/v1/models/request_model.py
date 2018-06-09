import datetime
import string

from MaintenanceTrackerAPI.api.v1.database import db
from MaintenanceTrackerAPI.api.v1.exceptions import RequestTransactionError


class Request(object):
    """
    This class handles the request object and all its functions.

    :param: user -> a user dictionary.
    :param: request_type -> the type of request, either 'Maintenance'
     or 'Repair'
    :param: title -> a short title that summarizes the object(s)
     being repaired or maintained
    :param: description -> a brief description of what is supposed to be repaired or
    maintained
    """

    def __init__(self, user: dict, request_type: str,
                 title: str, description: str):
        # Return 403 (Forbidden!) when Administrator tries to make a request
        if user['role'] != 'Consumer':
            raise RequestTransactionError(
                'Administrators cannot make requests!', 403)

        # check the request given, return 400 if its not in the list
        types_list = ['Maintenance', 'Repair']
        if bool(request_type) and request_type not in types_list:
            raise RequestTransactionError(
                'Cannot recognize the request type given :{}'.format(
                    request_type))

        # try and validate the given data before making the request
        try:
            self.__validate_request_details('title', title)
            self.__validate_request_details('description', description)
        except AssertionError as a:
            raise RequestTransactionError(a.args[0])

        # try and find a request with similar title and description in the
        # database
        db.cur = db.conn.cursor()
        sql = 'select(title, description) from requests where (title =%s and' \
              ' description=%s)'
        data = (title, description)
        try:
            db.cur.execute(sql, data)
            request = db.cur.fetchall()
            if request:
                raise RequestTransactionError('similar request exists')
        except Exception:
            pass
        # TODO check for the request status to allow re-submission
        # of a request that has already been resolved/rejected

        self.user_id = user['user_id']
        self.type = request_type if (bool(request_type)) else 'Repair'
        self.title = title
        self.description = description
        self.status = 'Pending Approval'
        self.date_requested = datetime.datetime.now()
        self.last_modified = None
        self.requested_by = user['email']
        self.__save()

    def __save(self):
        """
        Saves the the request in the database
        :return:
        """
        db.save_request(self)

    @staticmethod
    def __validate_request_details(name: str, item: str):
        """
            Used to validate title or description depending on the context given
            :param name: the context of validation
            :param item: item to be validated
            :rtype None
        """
        max_length, min_length = None, None

        if name == 'title':  # set the title's min and max length
            max_length = 70
            min_length = 10
        elif name == 'description':  # set the description min and max length
            max_length = 250
            min_length = 40

        # raise an error if the title or description given violates the min or
        # max length guidelines
        if len(item) > max_length:
            raise AssertionError('{0} too long. Max of {1} characters'
                                 ' allowed'.format(name, max_length))
        if len(item) < min_length:
            raise AssertionError('{0} too short. Min of {1} characters'
                                 ' allowed'.format(name, min_length))

        # check whether the title or description starts with a letter,
        # number, ',",or(
        if item[0] not in list(string.ascii_letters) + list(string.digits) \
                + ['\'', '\"', '(']:
            raise AssertionError('please enter a valid {}'.format(name))

        # check whether the title or description end with a letter, number,
        # ',",or(
        if str(item[-1]) not in list(string.ascii_letters) + \
                list(string.digits) + list('\'\").?!'):
            raise AssertionError('please enter a valid {}'.format(name))

        # generate a list of words for the validation item with white space
        # as delimiter
        item_words = item.split(' ')

        for word in item_words:
            if word.count('.') > 3:  # this means that there are more than three
                # consecutive full stops
                raise AssertionError(
                    'please check the punctuation in your {}'.format(name))

            if not word:  # this means there is extra space which is not needed
                raise AssertionError('Please check the'
                                     ' spacing on your {}'.format(name))

            # generate a list of characters from each word and check punctuation
            char_list = list(word)

            # the code below checks for unwanted subsequent punctuations
            for i in range(len(char_list) - 1):
                if char_list[i] in string.punctuation and char_list[i] != '.':
                    if char_list[i] in ['!', '?', '.'] and char_list[i + 1] in \
                            ['\'', '\"']:
                        continue
                    if char_list[i + 1] in string.punctuation \
                            and char_list[i] != '.':
                        raise AssertionError('please check the punctuation in'
                                             ' your {}'.format(name))
