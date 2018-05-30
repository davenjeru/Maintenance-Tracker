import datetime
import string

from .user_model import Consumer

requests_list = []


class RequestTransactionError(BaseException):
    """
    This is the exception raised when an error occurs during any request transaction.

    :param: msg: str -> The error message
    :param: abort_code: int -> The HTTP response code that is relevant to this error default 400 (Bad Request)
    """

    def __init__(self, msg: str, abort_code: int = 400):
        self.msg = msg
        self.abort_code = abort_code


class Request(object):
    """
    This class handles the request object and all its functions.

    :param: user -> a user object.
    :param: request_type -> the type of request, either 'Maintenance' or 'Repair'
    :param: title -> a short title that summarizes the object(s) being repaired or maintained
    :param: description -> a brief description of what is supposed to be repaired or maintained
    """
    id = 1

    def __init__(self, user: Consumer, request_type: str, title: str, description: str):
        # Return 403 (Forbidden!) when Administrator tries to make a request
        if user.role != 'Consumer':
            raise RequestTransactionError('Administrators cannot make requests!', 403)

        try:
            self.__validate_request_details('title', title)
            self.__validate_request_details('description', description)
        except AssertionError as a:
            raise RequestTransactionError(a.args[0])

        for post in requests_list:
            if post.title == title and post.description == description:
                raise RequestTransactionError('similar post exists')

        self.id = Request.id
        self.user_id = user.id
        self.type = request_type
        self.title = title
        self.description = description
        self.status = 'Pending Approval'
        self.date_requested = datetime.datetime.now()
        self.last_modified = None
        self.__save()

    def __save(self):
        Request.id += 1
        requests_list.append(self)

    @staticmethod
    def __validate_request_details(name: str, item: str):
        """
            Used to validate title or description depending on the context given
            :param name: the context of validation
            :param item: item to be validated

        """
        max_length, min_length = None, None

        if name == 'title':
            max_length = 70
            min_length = 10
        elif name == 'description':
            max_length = 250
            min_length = 40
        if len(item) > max_length:
            raise AssertionError('{0} too long. Max of {1} characters allowed'.format(name, max_length))
        if len(item) < min_length:
            raise AssertionError('{0} too short. Min of {1} characters allowed'.format(name, min_length))

        # check whether the title or description starts with a letter, number, ',",or(
        if item[0] not in list(string.ascii_letters) + list(string.digits) + ['\'', '\"', '(']:
            raise AssertionError('please enter a valid {}'.format(name))

        # check whether the title or description end with a letter, number, ',",or(
        if str(item[-1]) not in list(string.ascii_letters) + list(string.digits) + list('\'\").?!'):
            raise AssertionError('please enter a valid {}'.format(name))

        # generate a list of words for the validation item with white space as delimiter
        item_words = item.split(' ')

        for word in item_words:
            if not word:  # this means there is extra space
                raise AssertionError('Please check the spacing on your {}'.format(name))

            # generate a list of characters from each word and check punctuation
            char_list = list(word)
            for i in range(len(char_list) - 1):
                if char_list[i] in string.punctuation and char_list[i] != '.':
                    if char_list[i] in ['!', '?', '.'] and char_list[i + 1] in ['\'', '\"']:
                        continue
                    if char_list[i + 1] in string.punctuation and char_list[i] != '.':
                        raise AssertionError('please check the punctuation in your {}'.format(name))
