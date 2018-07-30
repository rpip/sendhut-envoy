import logging

from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from sendhut.envoy.core import (
    get_delivery_quote,
    get_scheduling_slots
)
from sendhut.utils import generate_password_token
from sendhut import notifications
from .base import serialize
from .permissions import NoPermission
from .validators import (
    LoginValidator,
    AddressValidator,
    UserCreateValidator,
    PasswordResetValidator,
    PasswordChangeValidator,
    DeliveryQuoteValidator,
    DeliveryValidator
)
from .serializers import (
    UserSerializer,
    AddressSerializer,
    DeliveryQuoteSerializer,
    DeliverySerializer,
    CourierSerializer,
    PickupSerializer,
    DropoffSerializer,
    ZoneSerializer,
    BatchSerializer,
    CancellationSerializer
)
from .exceptions import ValidationError, AuthenticationError
from .utils import create_user, authenticate

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

DEFAULT_AUTHENTICATION = (TokenAuthentication,)


logger = logging.getLogger(__name__)


class Endpoint(APIView):
    authentication_classes = DEFAULT_AUTHENTICATION
    renderer_classes = (JSONRenderer, )
    parser_classes = (JSONParser, )
    permission_classes = (NoPermission, )

    def respond(self, context=None, **kwargs):
        return Response(context, **kwargs)


class AuthToken(Endpoint):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        validator = LoginValidator(data=request.data)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        user = authenticate(**validator.data)
        if not user:
            raise AuthenticationError()

        token, created = Token.objects.get_or_create(user=user)
        data = {'token': token.key, 'user': serialize(user)}
        return self.respond(data)


class UserCreate(Endpoint):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        validator = UserCreateValidator(data=request.DATA)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        user = create_user(**validator.object)
        return self.respond({
            'token': user.auth_token.key,
            'user': serialize(user)
        })


class Schedules(Endpoint):
    def get(self, request, city=None, type=None, date=None, format=None):
        schedules = get_scheduling_slots(city, type, date)
        return self.respond(schedules)
