from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from sendhut.accounts.models import User
from sendhut.addressbook.models import Address
from .serializers import UserSerializer, AddressSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


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
