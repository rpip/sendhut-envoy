from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from sendhut.envoy.core import (
    get_delivery_quote, get_scheduling_slots)
from sendhut.utils import generate_password_token
from sendhut import notifications
from .utils import change_password
from .serializers import (
    UserSerializer, UserDetailsSerializer, DeliveryQuoteSerializer,
    PasswordResetSerializer, PasswordChangeSerializer
)
# from .exceptions import ValidationError, LookupError

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


def ok(data):
    return Response(data)


class AuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return ok({'token': token.key, 'user': UserSerializer(user).data})


class UserCreate(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return ok({
            'token': user.auth_token.key,
            'user': UserSerializer(user).data
        })


class PasswordResetView(APIView):
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.send_password_notification(serializer.validated_data["username"])
        # Return the success message with OK HTTP status
        return ok({"message": "Password reset e-mail has been sent."})

    def send_password_notification(self, user):
        token = generate_password_token(user.email)
        notifications.send_password_reset(user.email, token)


class PasswordChangeView(APIView):
    """
    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return ok({"detail": "New password has been saved."})

    def change_password(self, user):
        change_password(user)


class UserDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return ok(serializer.data)

    def put(self, request):
        serializer = UserDetailsSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ok(UserSerializer(serializer.instance).data)


class LogoutView(APIView):
    """
    Delete the Token object assigned to the current User object.
    Accepts/Returns nothing.
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        return ok({"message": "Successfully logged out."})


class Quotes(APIView):
    # TODO(yao): include price categories: ASAP or scheduled
    # TODO: change to serializer type
    def post(self, request):
        "Get delivery quote."
        serializer = DeliveryQuoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quote = get_delivery_quote(**serializer.validated_data)
        return ok(quote)


class Delivery(APIView):
    """
    List all deliveries, or create a new one.
    """
    # TODO(yao): filter by state: ongoing, scheduled, finished
    def get(self, request, format=None):
        user = request.user
        status = request.data.get('status')
        deliveries = get_deliveries(user, status)
        return ok(deliveries)

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


class Schedules(APIView):
    def get(self, request, city=None, type=None, date=None, format=None):
        return ok(get_scheduling_slots(city, type, date))
