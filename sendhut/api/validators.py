# https://github.com/getsentry/sentry/blob/master/src/sentry/api/endpoints/user_subscriptions.py#L59
from datetime import datetime
from dateutil.parser import parse

from rest_framework import serializers
from sendhut.accounts.utils import get_user
from sendhut.envoy import PackageTypes


ValidationError = serializers.ValidationError


class ProfileValidator(serializers.Serializer):
    company = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
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

    def validate_phone(self, value):
        if get_user(value):
            raise ValidationError("This phone number is already taken")

        return value

    def validate_email(self, value):
        if get_user(value):
            raise ValidationError("This email is already taken")

        return value


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
    username = serializers.CharField(max_length=128, required=True)
    old_password = serializers.CharField(max_length=128, required=True)
    new_password1 = serializers.CharField(max_length=128, required=True)
    new_password2 = serializers.CharField(max_length=128, required=True)

    def validate_new_password1(self, value):
        if value != self.initial_data['new_password2']:
            raise ValidationError('Invalid password')

        return value


class QuotesValidator(serializers.Serializer):
    # transport_type, package_size
    pickup = serializers.CharField(required=False)
    dropoffs = serializers.ListField(
        child=serializers.CharField(), min_length=1, max_length=4)


class AddressValidator(serializers.Serializer):
    address = serializers.CharField(max_length=120, required=True)
    # apt number or company name
    apt = serializers.CharField(max_length=42, required=False)
    notes = serializers.CharField(max_length=252, required=False)


class ContactValidator(serializers.Serializer):
    first_name = serializers.CharField(max_length=120, required=True)
    last_name = serializers.CharField(max_length=120, required=True)
    phone = serializers.CharField(max_length=30, required=True)
    email = serializers.CharField(max_length=40, required=False)
    address = AddressValidator(required=False)


class PickupValidator(serializers.Serializer):
    address = AddressValidator(required=True)
    pickup_time = serializers.CharField(required=True)
    # instructions for courier
    notes = serializers.CharField(required=False)
    contact = ContactValidator(required=False)

    def validate_pickup_time(self, value):
        if value == 'asap':
            return datetime.now()

        return parse(value)


class DropoffValidator(serializers.Serializer):
    address = AddressValidator(required=True)
    size = serializers.ChoiceField(
        choices=list(dict(PackageTypes.CHOICES).keys()), required=False)
    # instructions for courier
    notes = serializers.CharField(required=False)
    contact = ContactValidator(required=False)


class DeliveryValidator(serializers.Serializer):
    pickup = PickupValidator(required=True)
    dropoffs = serializers.ListField(
        child=DropoffValidator(required=True), min_length=1, max_length=4
    )
    quote = serializers.CharField(required=False)
    notes = serializers.CharField(required=False)
