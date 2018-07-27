from rest_framework import serializers
from sendhut.accounts.models import User
from sendhut.accounts.utils import get_user
from sendhut.addressbook.models import Address
from sendhut.envoy.models import DeliveryQuote, Delivery

from .utils import create_user


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('address', 'apt', 'location', 'photo', 'notes')


class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    username = serializers.CharField(required=False)
    phone = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'addresses',
                  'username', 'phone', 'last_login', 'identity_verified',
                  'is_active', 'date_joined', 'password')

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return create_user(
            phone=validated_data['phone'],
            email=validated_data['email'],
            password=validated_data['password']
        )


class UserDetailsSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'phone')


class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField()
    # maybe use SMS token to confirm password reset?

    def validate_username(self, value):
        # check if email or phone exist
        user = get_user(value)
        if not user:
            raise serializers.ValidationError('No user found')

        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        if not self.user.check_password(value):
            raise serializers.ValidationError('Invalid password')

    def save(self):
        self.user.set_password(self.validated_data['password'])
        self.user.save()


class DeliveryQuoteSerializer(serializers.ModelSerializer):

    pickup = serializers.CharField(required=False)
    dropoffs = serializers.ListField(
        child=serializers.CharField(), min_length=1, max_length=4)

    class Meta:
        model = DeliveryQuote
        fields = ('pickup', 'dropoffs', 'eta', 'fee', 'expires')


class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        fields = ('pickup', 'dropoff', 'quote', 'notes')

    def create(self, validated_data):
        # user = User(
        #     email=validated_data['email'],
        #     username=validated_data['username']
        # )
        # user.set_password(validated_data['password'])
        # user.save()
        # return user
        pass
