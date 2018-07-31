# https://github.com/getsentry/sentry/blob/master/src/sentry/api/endpoints/user_subscriptions.py#L59
from rest_framework import serializers
from sendhut.accounts.utils import get_user

ValidationError = serializers.ValidationError


class AddressValidator(serializers.Serializer):
    address = serializers.CharField(max_length=120)
    # apt number or company name
    apt = serializers.CharField(max_length=42, required=False)
    notes = serializers.CharField(max_length=252, required=False)


class LoginValidator(serializers.Serializer):
    username = serializers.CharField(required=True)
    # Use a minimum of 8 characters
    password = serializers.CharField(min_length=8, required=True)


class UserCreateValidator(serializers.Serializer):
    phone = serializers.CharField(max_length=20, required=True)
    # Use a minimum of 8 characters
    password = serializers.CharField(min_length=8, required=True)
    email = serializers.EmailField(required=False)
    name = serializers.CharField(required=False)


class PasswordResetValidator(serializers.Serializer):
    # can be email or phone. if phone, send sms else email
    username = serializers.CharField(max_length=20)
    # maybe use SMS token to confirm password reset?

    def validate_username(self, value):
        # check if email or phone exist
        user = get_user(value)
        if not user:
            raise ValidationError('No user found')

        return user


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


class DeliveryValidator(serializers.ModelSerializer):
    pickup = serializers.CharField(required=True)
    dropoff = serializers.CharField(required=True)
    quote = serializers.CharField(required=False)
    notes = serializers.CharField(required=False)
