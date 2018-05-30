import datetime
import string

from .user_model import Consumer, Admin

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

        for request in requests_list:
            if request.title == title and request.description == description:
                raise RequestTransactionError('similar request exists')
        # TODO check for the request status to allow re-submission of a request that has already been resolved/rejected

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

    def approve(self, user: Admin):

        # check the role of the user
        self.__check_for_admin(user)

        # check the status of the request
        if self.status != 'Pending Approval':
            raise RequestTransactionError('cannot approve a request which is {}'.format(self.status))

        self.status = 'Approved'
        self.last_modified = datetime.datetime.now()

    def reject(self, user: Admin):
        # check the role of the user
        self.__check_for_admin(user)

        # check the status of the request
        if self.status != 'Pending Approval':
            raise RequestTransactionError('cannot reject a request which is {}'.format(self.status))

        self.status = 'Rejected'
        self.last_modified = datetime.datetime.now()

    def in_progress(self, user: Admin):
        # check the role of the user
        self.__check_for_admin(user)

        # check the status of the request
        if self.status != 'Approved':
            raise RequestTransactionError('cannot in progress a request which is {}'.format(self.status))

        self.status = 'In Progress'
        self.last_modified = datetime.datetime.now()

    def resolve(self, user: Admin):
        self.__check_for_admin(user)

        # check the status of the request
        if self.status != 'In Progress':
            raise RequestTransactionError('cannot resolve a request which is {}'.format(self.status))

        self.status = 'Resolved'
        self.last_modified = datetime.datetime.now()

    def cancel(self, user: Consumer):
        # check the role of the user
        self.__check_for_consumer(user, 'cancel')

        # check the status of the request
        if self.status != 'Pending Approval':
            raise RequestTransactionError('cannot cancel a request which is {}'.format(self.status))

        self.status = 'Cancelled'
        self.last_modified = datetime.datetime.now()

    def edit(self, user: Consumer, details: dict):
        # check the role of the user
        self.__check_for_consumer(user, 'edit')

        # check whether this request belongs to the user given
        if user.id != self.user_id:
            raise RequestTransactionError('this request does not belong to the selected user', 403)

        # check the request status
        if self.status != 'Pending Approval':
            raise RequestTransactionError('cannot edit a request which is {}'.format(self.status))

        title = details.get('title', None)
        description = details.get('description', None)

        try:
            if title is not None:
                self.__validate_request_details('title', title)
            if description is not None:
                self.__validate_request_details('description', description)
        except AssertionError as e:
            raise RequestTransactionError(e.args[0])

        if title is not None:
            if self.title == title:
                name = 'title'
                raise RequestTransactionError('{0} given matches the previous {0}'.format(name))
        elif description is not None:
            if self.description == description:
                name = 'description'
                raise RequestTransactionError('{0} given matches the previous {0}'.format(name))

        for request in requests_list:
            if description is not None and request.description == description:
                raise RequestTransactionError('similar description exists')

        self.title = title if title is not None else self.title
        self.description = description if description is not None else self.description

        self.last_modified = datetime.datetime.now()
        return self

    def delete(self, user: Consumer):
        # check the role of the user
        self.__check_for_consumer(user, 'delete')

        # check the status of the request
        if self.status != 'Resolved' and self.status != 'Rejected' and self.status != 'Cancelled':
            raise RequestTransactionError('cannot delete a request which is {}'.format(self.status))

        requests_list.remove(self)
        del self
        return True

    @staticmethod
    def __check_for_admin(user):
        if user.role != 'Administrator':
            raise RequestTransactionError('{} not allowed to change request status'.format(user.role))

    @staticmethod
    def __check_for_consumer(user, context: str):
        if user.role != 'Consumer':
            raise RequestTransactionError('{0} not allowed to {1} request'.format(user.role, context))
