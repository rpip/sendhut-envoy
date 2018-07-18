from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from sendhut.accounts.models import User
from sendhut.addressbook.models import Address
from sendhut.envoy.core import get_delivery_quote
from .serializers import UserSerializer, AddressSerializer
from . import DeliveryQuoteRequest
from .exceptions import ValidationError, LookupError


def ok(data):
    return Response(data)


def fail(err):
    return Response(err._error)


class AuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class Quotes(APIView):
    """
    View get delivery quote.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # TODO(yao): show price categories: ASAP, same day or next day, scheduled
    def post(self, request, format=None):
        valid, data = DeliveryQuoteRequest(request.data).is_valid()
        if valid:
            try:
                quote = get_delivery_quote(**data)
            except:
                raise LookupError

            return ok(quote)

        raise ValidationError(details=data)


class Delivery(APIView):
    """
    List all deliveries, or create a new one.
    """
    # TODO(yao): filter by state: ongoing, scheduled, finished
    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


class DeliveryDetail(APIView):
    """
    Retrieve, update or delete a delivery instance.
    """
    pass


class Payment(APIView):
    """
    Pay from Sendhut credits or direct pay
    If you do more than 50 weekly, you earn credits

    - invoices
    - new invoice
    - sendhut credits
    - payment history
    """
    pass


class ProfileDetail(APIView):
    """
    Create, retrieve and update profiles
    """
    pass
