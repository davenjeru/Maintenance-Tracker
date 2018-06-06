class UserTransactionError(BaseException):
    """
    This is the exception raised when an error occurs during
     any user transaction.

    :param: msg: str -> The error message
    :param: abort_code: int -> The HTTP response code that is relevant to this
     error default 400 (Bad Request)
    """

    def __init__(self, msg: str, abort_code: int = 400):
        self.msg = msg
        self.abort_code = abort_code


class RequestTransactionError(BaseException):
    """
    This is the exception raised when an error occurs during any request
    transaction.

    :param: msg: str -> The error message :param: abort_code: int -> The HTTP
    response code that is relevant to this error default 400 (Bad Request)
    """

    def __init__(self, msg: str, abort_code: int = 400):
        self.msg = msg
        self.abort_code = abort_code


class PayloadExtractionError(BaseException):
    """
    Custom exception that will be raised if there is an error
    during payload extraction
    """

    def __init__(self, msg: str, abort_code: int = 400):
        self.msg = msg
        self.abort_code = abort_code
