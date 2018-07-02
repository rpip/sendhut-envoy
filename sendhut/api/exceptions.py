from collections import namedtuple
from http import HTTPStatus
from django.utils import six

from sendhut.utils import to_serializable


ErrorDetail = namedtuple('ErrorDetail', ['kind', 'code', 'message', 'details'])


def _get_error_details(code, message, details):
    err = ErrorDetail(
        kind='error', code=code, message=message, details=details)
    return err._asdict()


class APIException(Exception):
    """
    Base class for API exceptions.
    Subclasses should provide `code` and `detail` properties.
    """
    http_code = HTTPStatus.INTERNAL_SERVER_ERROR
    message = 'A server error occurred.'
    code = 'error'
    details = {}

    def __init__(self, code=None, message=None, details=None):
        self.code = code or self.code
        self.message = message or self.message
        self.details = details or self.details

        self._error = _get_error_details(self.code, self.message, self.details)

    def __str__(self):
        return six.text_type(self._error)


class ValidationError(APIException):
    http_code = HTTPStatus.BAD_REQUEST
    code = 'invalid_params'
    message = 'The parameters of your request were missing or invalid.'


@to_serializable.register(APIException)
def ts_api_error(err):
    return err._error
