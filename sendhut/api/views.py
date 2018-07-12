from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from schematics.exceptions import DataError

from sendhut.accounts.models import User
from sendhut.addressbook.models import Address
from sendhut.envoy.core import get_delivery_quote
from .serializers import UserSerializer, AddressSerializer
from . import DeliveryQuoteRequest
from .exceptions import ValidationError


def ok(data):
    return Response(data)


def fail(err):
    return Response(err._error)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class DeliveryQuote(APIView):
    """
    View get delivery quote.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    def post(self, request, format=None):
        dv_req = DeliveryQuoteRequest(request.data)
        try:
            dv_req.validate()
            quote = get_delivery_quote(**dv_req.to_primitive())
            return ok(quote)
        except DataError as ex:
            details = {k: v.to_primitive() for k, v in ex.messages.items()}
            return fail(ValidationError(details=details))


class AuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        # username = request.META.get('X_USERNAME')
        # TODO(yao): support basic auth for GT
        # TODO(yao): create custom permissions class to check non-internal keys
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # TODO(yao): return custom sendhut response
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

    def basic_auth(self, request):
        pass
