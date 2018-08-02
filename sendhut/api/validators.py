# https://github.com/getsentry/sentry/blob/master/src/sentry/api/endpoints/user_subscriptions.py#L59
from rest_framework import serializers
from sendhut.accounts.utils import get_user

ValidationError = serializers.ValidationError


class ProfileValidator(serializers.Serializer):
    company = serializers.CharField(required=False)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    email = serializers.CharField(required=False)


class LoginValidator(serializers.Serializer):
    username = serializers.CharField(required=True)
    # Use a minimum of 8 characters
    password = serializers.CharField(min_length=8, required=True)


class UserCreateValidator(serializers.Serializer):
    phone = serializers.CharField(max_length=20, required=True)
    # Use a minimum of 8 characters
    password = serializers.CharField(min_length=8, required=True)
    email = serializers.EmailField(required=False)

    def validate_phone(self, data):
        if get_user(data):
            raise ValidationError("This phone number is already taken")

    def validate_email(self, data):
        if get_user(data):
            raise ValidationError("This email is already taken")


class PasswordResetValidator(serializers.Serializer):
    # can be email or phone. if phone, send sms else email
    username = serializers.CharField(max_length=20)

    def validate_username(self, value):
        # check if email or phone exist
        user = get_user(value)
        if not user:
            raise ValidationError('No user found')

        return value


class PasswordChangeValidator(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, required=True)
    new_password1 = serializers.CharField(max_length=128, required=True)
    new_password2 = serializers.CharField(max_length=128, required=True)

    def validate_old_password(self, value):
        if not self.user.check_password(value):
            raise serializers.ValidationError('Invalid password')

    def validate_new_password1(self, value):
        if value != self.data['new_password2']:
            raise ValidationError('Invalid password')


class QuotesValidator(serializers.Serializer):
    pickup = serializers.CharField(required=False)
    dropoffs = serializers.ListField(
        child=serializers.CharField(), min_length=1, max_length=4)


class AddressValidator(serializers.Serializer):
    address = serializers.CharField(max_length=120)
    # apt number or company name
    apt = serializers.CharField(max_length=42, required=False)
    notes = serializers.CharField(max_length=252, required=False)


class ContactValidator(serializers.Serializer):
    first_name = serializers.CharField(max_length=120, required=True)
    last_name = serializers.CharField(max_length=120, required=True)
    phone = serializers.CharField(max_length=30, required=False)
    email = serializers.CharField(max_length=40, required=False)
    address = AddressValidator(required=False)


class PickupValidator(serializers.Serializer):
    address = AddressValidator(required=True)
    # instructions for courier
    notes = serializers.CharField(required=False)
    contact = ContactValidator(required=False)


class DropoffValidator(serializers.Serializer):
    address = AddressValidator(required=True)
    # instructions for courier
    notes = serializers.CharField(required=False)
    contact = ContactValidator(required=False)


class DeliveryValidator(serializers.Serializer):
    pickup = PickupValidator(required=True)
    dropoff = DropoffValidator(required=True)
    quote = serializers.CharField(required=False)
    notes = serializers.CharField(required=False)
