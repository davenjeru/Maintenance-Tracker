import re
import string

from werkzeug.security import generate_password_hash

from MaintenanceTrackerAPI.api.v1.database import Database
from MaintenanceTrackerAPI.api.v1.exceptions import UserTransactionError

db = Database()


class User:
    """
    This is the user class.
    Defines how a user is created and saved in the database
    """

    def __init__(self, email: str, password: str, security_question: str,
                 security_answer: str, role: str = 'Consumer'):

        # validate the details given
        try:
            self._validate_user_details('email', email)
            self._validate_user_details('password', password)
            self._validate_user_details('security question', security_question)
            self._validate_user_details('security answer', security_answer)
        except AssertionError as a:
            raise UserTransactionError(a.args[0])

        # Look for a user with similar email in the database
        if db.get_user_by_email(email) is not None:
            raise UserTransactionError('user with similar email exists', 409)

        self.email = email
        self.password_hash = generate_password_hash(password)
        self.security_question = security_question
        self.security_answer_hash = generate_password_hash(security_answer)
        self.role = role
        self.__save()

    def __save(self):
        """
        Saves the user in the database
        """
        db.save_user(self)

    @staticmethod
    def _validate_user_details(name: str, item: str):
        """
        Validates input depending on the given context
        :param name: context of validation
        :param item: item to be validated
        """

        if not item:  # this means that the function was called with the
            # required parameter set as None
            raise AssertionError('missing \"{0}\" parameter'.format(name))

        def validate_security_question_or_answer(context: str,
                                                 validation_item: str):

            # set max and min length out here so that it will be easier to
            # validate later
            max_length, min_length = None, None

            if context == 'security question':
                max_length = 50
                min_length = 10

                # Check whether security question starts with 'Wh' or 'Are'
                if validation_item[0] not in list('WwAa'):
                    raise AssertionError('{} must start with a \'Wh\' or a'
                                         ' \'Are\' question'.format(context))

                # check whether security question ends with a question mark
                if validation_item[-1] != '?':
                    raise AssertionError('{} must end with a question mark'
                                         ' \'?\''.format(context))

                # make sure there are no punctuations in between
                for char in list(validation_item[:-1]):
                    if char in string.punctuation:
                        raise AssertionError('{} must not contain any'
                                             ' punctuations mid'
                                             ' sentence'.format(context))

            if context == 'security answer':
                max_length = 20
                min_length = 5

                # security answer should not have any punctuations
                for char in list(validation_item):
                    if char in string.punctuation:
                        raise AssertionError('{} must not contain any'
                                             ' punctuations'.format(context))

            # this is where length is checked to avoid checking twice
            if len(validation_item) < min_length:
                raise AssertionError('{0} is too short. Min of {1}'
                                     ' characters'.format(context, min_length))
            if len(validation_item) > max_length:
                raise AssertionError('{0} too long. Max of {1}'
                                     ' characters'.format(context, max_length))

            # check for spacing issues
            for word in validation_item.split(' '):
                if not word:
                    raise AssertionError('Please check the spacing on your'
                                         ' {}'.format(context))

        # use regular expressions to validate email and password
        email_pattern = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        password_pattern = re.compile(
            r"(?=^.{12,80}$)(?=.*\d)"
            r"(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^;*()_+}{:'?/.,])(?!.*\s).*$")

        if name == 'email':
            if not bool(email_pattern.match(item)):
                raise AssertionError('email address syntax is invalid')
        elif name == 'password':
            if not bool(password_pattern.match(item)):
                raise AssertionError('password syntax is invalid')
        elif name == 'security question' or name == 'security answer':
            validate_security_question_or_answer(name, item)
