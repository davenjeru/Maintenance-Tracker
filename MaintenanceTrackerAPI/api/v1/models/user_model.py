import re

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
                self.password_hash = generate_password_hash(new_password)
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

        email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        password_pattern = re.compile(
            r"(?=^.{12,80}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^;*()_+}{:'?/.,])(?!.*\s).*$")

        if not item:
            raise AssertionError('missing \"{0}\" parameter'.format(name))

        if name == 'email':
            if not bool(email_pattern.match(item)):
                raise AssertionError('email address syntax is invalid')
        elif name == 'password':
            if not bool(password_pattern.match(item)):
                raise AssertionError('password syntax is invalid')


class Consumer(User):
    pass


class Admin(User):
    pass
