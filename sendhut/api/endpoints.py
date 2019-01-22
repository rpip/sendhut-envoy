import logging

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from sendhut.utils import update_model_fields, generate_token
import sendhut.accounts.utils as auth
from sendhut import sms, factory
from sendhut.payments import utils as Payments
from sendhut.envoy.core import (
    get_delivery_quote,
    get_delivery_quotev1,
    get_scheduling_slots
)
from .base import serialize
# import serializers so they're hooked to the serialize function
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
    CancellationSerializer,
    TransactionSerializer,
    WalletSerializer,
    MoneySerializer
)
from .validators import (
    SMSTokenValidator,
    LoginValidator,
    ProfileValidator,
    QuotesV1Validator,
    QuotesValidator,
    DeliveryValidator,
    ContactValidator,
    WalletTopUpValidator,
    ChargeRefValidator
)
from .exceptions import ValidationError, AuthenticationError
from sendhut.envoy.models import Delivery
from sendhut.envoy.core import create_delivery
from sendhut.addressbook.models import Contact


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
        validator = SMSTokenValidator(data=request.data)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        phone = validator.data.get("phone")
        user = auth.get_user(phone)
        signup = False
        if not user:
            # first-time user, create account
            signup = True
            user = auth.create_user(phone)

        token, created = Token.objects.get_or_create(user=user)
        data = {'token': token.key, 'user': serialize(user), 'signup': signup}
        return self.respond(data)


class LoginEndpoint(Endpoint):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        validator = LoginValidator(data=request.data)
        if not validator.is_valid():
            raise AuthenticationError(details=validator.errors)

        phone_number = validator.data.get("phone")
        if auth.is_demo_number(phone_number):
            token = auth.set_auth_token(phone_number, False)
        else:
            token = auth.set_auth_token(phone_number)
            sms.push_verification_sms(phone_number, token)

        return self.respond({'status': 'OK', 'code': token})


class LogoutEndpoint(Endpoint):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        auth.logout(request.user)
        return self.respond({'status': 'OK'})


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
        logger.debug("Quotes Request DATA: %s", request.data)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        # todo(yao): save Quote in DB, valid for x minutes
        quote = get_delivery_quote(**validator.validated_data)
        phone = request.user.phone
        payment_ref = Payments.get_charge_ref(phone, quote["pricing_int"])
        return self.respond(serialize(dict(payment_ref=payment_ref, **quote)))


class ChargeRefEndpoint(Endpoint):
    """
    Returns the access code to be used to create a charge on a card.
    """
    def post(self, request):
        validator = ChargeRefValidator(data=request.data)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        amount = validator.data['amount']
        ref = Payments.get_charge_ref(request.user.phone, amount)
        return self.respond(ref)


class DeliveryEndpoint(Endpoint):

    def get(self, request, status=None, *args, **kwargs):
        status = request.query_params.get('status')
        deliveries = Delivery.for_user(request.user, status)
        ds = serialize([x for x in deliveries])
        return self.respond(ds)

    def post(self, request):
        validator = DeliveryValidator(data=request.data)
        logger.debug("Delivery Request DATA: %s", request.data)
        if not validator.is_valid():
            logger.debug("Delivery Errors: %s", validator.errors)
            raise ValidationError(details=validator.errors)

        batch = create_delivery(user=request.user, **validator.data)
        # TODO: POST delivery task to driver delivery engine: onfleet/tookan etc.
        return self.respond(serialize(batch))


class DeliveryDetailEndpoint(Endpoint):

    def get(self, request, delivery_id, *args, **kwargs):
        delivery = Delivery.objects.get(id=delivery_id)
        return self.respond(serialize(delivery))

    def patch(self, request, delivery_id, *args, **kwargs):
        validator = DeliveryValidator(data=request.data)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        delivery = update_model_fields(delivery_id, validator.data)
        return self.respond(serialize(delivery))


class AddressBookEndpoint(Endpoint):

    def get(self, request):
        contacts = request.user.get_contacts()
        return self.respond(serialize(contacts))

    def post(self, request):
        validator = ContactValidator(data=request.data)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        contact = Contact.objects.create(**validator.data)
        return self.respond(serialize(contact))


class ContactDetailEndpoint(Endpoint):

    def get(self, request, contact_id, *args, **kwargs):
        contact = Contact.objects.get(id=contact_id)
        return self.respond(serialize(contact))


class WalletTopUpEndpoint(Endpoint):

    def post(self, request):
        validator = WalletTopUpValidator(data=request.data)
        if not validator.is_valid():
            raise ValidationError(details=validator.errors)

        amount = validator.data['amount']
        ref = validator.data['reference']
        wallet = request.user.service_wallet
        # todo: refactor
        txn = Payments.fund_wallet(wallet, amount, ref)
        response = dict(balance=wallet.balance.amount, **serialize(txn))
        return self.respond(serialize(response))
