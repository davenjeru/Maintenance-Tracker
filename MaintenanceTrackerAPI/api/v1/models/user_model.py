import re
import string

from werkzeug.security import generate_password_hash, check_password_hash

users_list = []


class UserTransactionError(BaseException):
    """
    This is the exception raised when an error occurs during any user transaction.

    :param: msg: str -> The error message
    :param: abort_code: int -> The HTTP response code that is relevant to this error default 400 (Bad Request)
    """

    def __init__(self, msg: str, abort_code: int = 400):
        self.msg = msg
        self.abort_code = abort_code


class User(object):
    """
        This is the user class.
        Defines a user and all actions that can be done by it.
        """

    id = 1

    def __init__(self, email: str, password: str, security_question: str, security_answer: str):

        try:
            self._validate_user_details('email', email)
            self._validate_user_details('password', password)
            self._validate_user_details('security question', security_question)
            self._validate_user_details('security answer', security_answer)
        except AssertionError as a:
            raise UserTransactionError(a.args[0])

        for user in users_list:
            if user.email == email:
                raise UserTransactionError('a user with similar email exists')

        self.email = email
        self.password_hash = generate_password_hash(password)
        self.id = User.id
        self.security_question = security_question
        self.security_answer = generate_password_hash(security_answer)
        self.__save()

    def __save(self):
        """
        Stores user in the users list
        """
        User.id += 1
        users_list.append(self)

    def authenticate(self, password: str):
        """
        :param password: The password to be checked
        :return: True if the password is correct, False otherwise
        :rtype: bool
        """
        return check_password_hash(self.password_hash, password)

    def reset_password(self, security_question: str, security_answer: str, new_password: str):
        """
        Enables user to reset password
        :param security_question: The security question that the user chose
        :param security_answer: The answer to the above question
        :param new_password: The new password to be set
        """
        if self.security_question == security_question:
            if check_password_hash(self.security_answer, security_answer):
                try:
                    self._validate_user_details('password', new_password)
                    self.password_hash = generate_password_hash(new_password)
                except AssertionError as a:
                    raise UserTransactionError(a.args[0])
            else:
                raise UserTransactionError('wrong security answer!')
        else:
            raise UserTransactionError('wrong security question!')

    @staticmethod
    def _validate_user_details(name: str, item: str):
        """
        Validates input depending on the given context
        :param name: context of validation
        :param item: item to be validated
        """

        def validate_security_question_or_answer(context: str, validation_item: str):

            # set max and min length out here so that it will be easier to validate later
            max_length, min_length = None, None

            if context == 'security question':
                max_length = 50
                min_length = 10

                # Check whether security question starts with 'Wh' or 'Are'
                if validation_item[0] not in list('WwAa'):
                    raise AssertionError('{} must start with a \'Wh\' or a \'Are\' question'.format(context))

                # check whether security question ends with a question mark
                if validation_item[-1] != '?':
                    raise AssertionError('{} must end with a question mark \'?\''.format(context))

                # make sure there are no punctuations in between
                for char in list(validation_item[:-1]):
                    if char in string.punctuation:
                        raise AssertionError('{} must not contain any punctuations mid sentence'.format(context))

            if context == 'security answer':
                max_length = 20
                min_length = 5

                # security answer should not have any punctuations
                for char in list(validation_item):
                    if char in string.punctuation:
                        raise AssertionError('{} must not contain any punctuations'.format(context))

            # this is where length is checked to avoid checking twice
            if len(validation_item) < min_length:
                raise AssertionError('{0} is too short. Min of {1} characters'.format(context, min_length))
            if len(validation_item) > max_length:
                raise AssertionError('{0} too long. Max of {1} characters'.format(context, max_length))

            # check for spacing issues
            for word in validation_item.split(' '):
                if not word:
                    raise AssertionError('Please check the spacing on your {}'.format(context))

        email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        password_pattern = re.compile(
            r"(?=^.{12,80}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^;*()_+}{:'?/.,])(?!.*\s).*$")

        if not item:  # this means that the function was called with the required parameter set as None
            raise AssertionError('missing \"{0}\" parameter'.format(name))

        if name == 'email':
            if not bool(email_pattern.match(item)):
                raise AssertionError('email address syntax is invalid')
        elif name == 'password':
            if not bool(password_pattern.match(item)):
                raise AssertionError('password syntax is invalid')
        elif name == 'security question' or name == 'security answer':
            validate_security_question_or_answer(name, item)


class Consumer(User):
    """
    This is the class that handles consumers.

    Consumers can:
    - Make requests
    - Edit requests
    - View their own requests
    - Delete requests
    """

    def __init__(self, email: str, password: str, security_question: str, security_answer: str):
        super().__init__(email, password, security_question, security_answer)
        self.__role = 'Consumer'
        self.__request_count = 0

    @property
    def role(self):
        return self.__role


class Admin(User):
    """
        This is the class that handles administrators.

        Administrators can:
        - View all requests made to the app
        - Update request statuses
    """

    def __init__(self, email: str, password: str, security_question: str, security_answer: str):
        super().__init__(email, password, security_question, security_answer)
        self.__role = 'Administrator'

    @property
    def role(self):
        return self.__role
