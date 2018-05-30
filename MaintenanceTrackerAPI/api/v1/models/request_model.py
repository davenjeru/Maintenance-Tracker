import datetime

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
        if user.role != 'Consumer':
            raise RequestTransactionError('Administrators cannot make requests!', 403)

        self.id = Request.id
        self.user_id = user.id
        self.type = request_type
        self.title = title
        self.description = description
        self.status = 'Pending Approval'
        self.date_requested = datetime.datetime.now()
        self.last_modified = None
