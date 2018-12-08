import logging

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from sendhut.utils import update_model_fields
from sendhut.accounts.utils import (
    create_user,
    authenticate,
    logout,
    trigger_password_reset,
    change_password
)
from sendhut.envoy.core import (
    get_delivery_quote,
    get_delivery_quotev1,
    get_scheduling_slots
)
from .base import serialize
from .permissions import NoPermission
from .validators import (
    LoginValidator,
    AddressValidator,
    UserCreateValidator,
    ProfileValidator,
    PasswordResetValidator,
    PasswordChangeValidator,
    QuotesV1Validator,
    QuotesValidator,
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
from sendhut.envoy.models import Delivery
from sendhut.envoy.core import create_delivery

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
    permission_classes = (IsAuthenticated,)

    def respond(self, context=None, **kwargs):
        return Response(context, **kwargs)


class AuthTokenEndpoint(Endpoint):
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


class LogoutEndpoint(Endpoint):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        logout(request.user)
        return self.respond({'status': 'OK'})


class PasswordResetEndpoint(Endpoint):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request):
        validator = PasswordResetValidator(data=request.data)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        trigger_password_reset(validator.data['username'])
        return self.respond({'message': 'Password reset sent'})


class PasswordChangeEndpoint(Endpoint):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        validator = PasswordChangeValidator(data=request.data)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        # if username is phone, send code to confirm else if email link
        username = validator.data['username']
        old_password = validator.data['old_password']
        new_password = validator.data['new_password1']
        change_password(username, old_password, new_password)
        return self.respond({'status': 'OK'})


class RegistrationEndpoint(Endpoint):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        validator = UserCreateValidator(data=request.data)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        user = create_user(**validator.data)
        return self.respond({
            'token': user.auth_token.key,
            'user': serialize(user)
        })


class ProfileEndpoint(Endpoint):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return self.respond(serialize(request.user))

    def patch(self, request):
        validator = ProfileValidator(data=request.data)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        user = request.user
        user = update_model_fields(user, validator.data)
        return self.respond(serialize(user))


class SchedulesEndpoint(Endpoint):
    permission_classes = (IsAuthenticated,)

    def get(self, request, city=None, type=None, date=None, format=None):
        schedules = get_scheduling_slots(city, type, date)
        return self.respond(schedules)


class QuotesV1Endpoint(Endpoint):
    permission_classes = ()

    def post(self, request):
        validator = QuotesV1Validator(data=request.data)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        quote = get_delivery_quotev1(**validator.validated_data)
        return self.respond(serialize(quote))


class QuotesEndpoint(Endpoint):
    permission_classes = ()

    def post(self, request):
        validator = QuotesValidator(data=request.data)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        quote = get_delivery_quote(**validator.validated_data)
        return self.respond(serialize(quote))


class DeliveryEndpoint(Endpoint):

    def get(self, request, status=None, *args, **kwargs):
        status = request.query_params.get('status')
        deliveries = Delivery.for_user(request.user, status)
        ds = serialize([x for x in deliveries])
        return self.respond(ds)

    def post(self, request):
        validator = DeliveryValidator(data=request.data)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        batch = create_delivery(user=request.user, **validator.data)
        # TODO: POST delivery task to driver delivery engine: onfleet/tookan etc.
        return self.respond(serialize(batch))


class DeliveryDetailEndpoint(Endpoint):

    def get(self, request, delivery_id, *args, **kwargs):
        delivery = Delivery.objects.get(id=delivery_id)
        return self.respond(serialize(delivery))
