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


class Consumer(User):
    pass


class Admin(User):
    pass

