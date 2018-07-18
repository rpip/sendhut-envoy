from collections import namedtuple
from http import HTTPStatus

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils import six
from rest_framework.response import Response
from rest_framework.views import set_rollback
from rest_framework import exceptions

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
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    message = 'A server error occurred.'
    # The type of error returned
    type = 'error'
    details = {}

    def __init__(self, code=None, message=None, details=None):
        self.code = code or self.code
        self.message = message or self.message
        self.details = details or self.details

        self._error = _get_error_details(self.code, self.message, self.details)

    def __str__(self):
        return six.text_type(self._error)


class ValidationError(APIException):
    code = HTTPStatus.BAD_REQUEST
    type = 'invalid_params'
    message = 'The parameters of your request were missing or invalid.'


class PermissionError(APIException):
    pass


class APIError(APIException):
    """
    API errors cover any other type of problem, such as:

    * Internal Server Error: Something went wrong on Sendhut's end.
    * Service Unavailable.
    """
    pass


class LookupError(APIException):
    code = HTTPStatus.NOT_FOUND
    type = 'lookup_error'
    message = 'Location not found'


class AuthenticationError(APIException):
    """
    Unauthorized: missing API key or invalid API key provided.
    """
    pass


@to_serializable.register(APIException)
def ts_api_error(err):
    return err._error


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.
    By default we `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.
    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if issubclass(exc.__class__, APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        data = exc._error

        set_rollback()
        return Response(data, status=exc.code, headers=headers)

    return None
