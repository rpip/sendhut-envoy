import re
from collections import namedtuple
from http import HTTPStatus

from django.core.exceptions import PermissionDenied as DjPermissionDenied
from django.db.utils import IntegrityError
from django.http import Http404
from django.utils import six
from rest_framework.response import Response
from rest_framework.views import set_rollback
from rest_framework import exceptions as drf_exceptions
from rest_framework import status

from sendhut.utils import to_serializable


ErrorDetail = namedtuple('ErrorDetail', ['kind', 'type', 'message', 'details'])


def _get_error_details(type, message, details):
    err = ErrorDetail(
        kind='error', type=type, message=message, details=details)
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

    def __init__(self, type=None, message=None, details=None):
        self.type = type or self.type
        self.message = message or self.message
        self.details = details or self.details

        self._error = _get_error_details(self.type, self.message, self.details)

    def __str__(self):
        return six.text_type(self._error)


class ValidationError(APIException):
    code = HTTPStatus.BAD_REQUEST
    type = 'invalid_params'
    message = 'The parameters of your request were missing or invalid.'


class PermissionDenied(APIException):
    code = status.HTTP_403_FORBIDDEN
    type = 'permission_denied'
    message = 'You do not have permission to perform this action.'


class APIError(APIException):
    """
    API errors cover any other type of problem, such as:

    * Internal Server Error: Something went wrong on Sendhut's end.
    * Service Unavailable.
    """
    pass


class UnknownLocation(APIException):
    code = HTTPStatus.NOT_FOUND
    type = 'unknown_location'
    message = """
    We weren't able to understand the provided address.
    This usually indicates the address is wrong, or perhaps not exact enough.
    """
    # TODO: include requested pickup & dropoffs in the details


class CouriersBusy(APIException):
    code = HTTPStatus.SERVICE_UNAVAILABLE
    type = 'couriers_busy'
    message = 'All of our couriers are currently busy.'


class AuthenticationError(APIException):
    """
    Authentication

    Unauthorized: missing API key or invalid API key provided.
    """
    code = status.HTTP_404_NOT_FOUND
    message = 'Invalid username or password'
    type = 'authentication_error'


class NotFound(APIException):
    code = status.HTTP_404_NOT_FOUND
    message = 'Not found.'
    type = 'not_found'


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
    _DRF_HANDLERS = {
        status.HTTP_404_NOT_FOUND: NotFound,
        status.HTTP_400_BAD_REQUEST: ValidationError,
        status.HTTP_401_UNAUTHORIZED: AuthenticationError,
        status.HTTP_403_FORBIDDEN: PermissionDenied
    }

    def _err(e):
        lambda e: [x['message'] for x in e]

    if isinstance(exc, Http404):
        exc = NotFound()
    elif isinstance(exc, DjPermissionDenied):
        exc = PermissionDenied()
    # elif isinstance(exc, LookupError):
    #     # get exact reason: unknown_location? etc
    #     exc = UnknownLocation()
    # handle DRF exceptions
    elif issubclass(exc.__class__, drf_exceptions.APIException):
        errors = [(k, _err(v)) for k, v in exc.get_full_details().items()]
        exc = _DRF_HANDLERS[exc.status_code](details=errors)

        set_rollback()
    elif isinstance(exc, IntegrityError):
        err_re = r'Key \((?P<column>\w+)\)=\((?P<value>\w+)\) already exists'
        m = re.search(err_re, exc.__cause__.diag.message_detail)
        column, value = m.groups()
        msg = "This {} is already taken".format(column)
        exc = APIError(message=msg, details={column: value})
    elif issubclass(exc.__class__, APIException):
        pass
    else:
        exc = APIError()

    return Response(exc._error, status=exc.code, headers={})
