# https://github.com/getsentry/sentry/blob/master/src/sentry/api/endpoints/user_subscriptions.py#L59
from datetime import datetime
from dateutil.parser import parse

from rest_framework import serializers
import sendhut.accounts.utils as auth
from sendhut.envoy import PackageTypes
from sendhut.payments import PaymentChannels


ValidationError = serializers.ValidationError


# class BaseSerializer(serializers.Serializer):
#     meta = dictionary field to hold arbitrary meta data
#     pass


class ProfileValidator(serializers.Serializer):
    company = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=True)
    email = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)


class LoginValidator(serializers.Serializer):
    # todo(yao): validate phone numbers
    phone = serializers.CharField(required=True)


class SMSTokenValidator(serializers.Serializer):
    code = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

    def validate_code(self, value):
        phone = self.initial_data.get("phone")
        if not auth.verify_token(phone, value):
            raise ValidationError("Invalid verification code")

        return value


class UserCreateValidator(serializers.Serializer):
    phone = serializers.CharField(max_length=20, required=True)
    # Use a minimum of 8 characters
    password = serializers.CharField(min_length=8, required=True)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def validate_phone(self, value):
        if auth.get_user(value):
            raise ValidationError("This phone number is already taken")

        return value

    def validate_email(self, value):
        if auth.get_user(value):
            raise ValidationError("This email is already taken")

        return value


class PasswordResetValidator(serializers.Serializer):
    # can be email or phone. if phone, send sms else email
    username = serializers.CharField(max_length=20)

    def validate_username(self, value):
        # check if email or phone exist
        user = auth.get_user(value)
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


class AddressValidator(serializers.Serializer):
    address = serializers.CharField(max_length=120, required=True)
    # apt number or company name
    apt = serializers.CharField(max_length=42, required=False)
    notes = serializers.CharField(max_length=252, required=False)
    meta = serializers.JSONField(required=False, allow_null=True)


class ContactValidator(serializers.Serializer):
    first_name = serializers.CharField(max_length=120, required=True)
    last_name = serializers.CharField(max_length=120, required=True)
    phone = serializers.CharField(max_length=30, required=True)
    email = serializers.CharField(
        max_length=40, required=False,
        allow_null=True, allow_blank=True)
    address = AddressValidator(required=False)


class PickupValidator(serializers.Serializer):
    address = AddressValidator(required=True)
    pickup_time = serializers.CharField(required=True)
    # instructions for courier
    notes = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    contact = ContactValidator(required=False)

    def validate_pickup_time(self, value):
        if value == 'asap':
            return datetime.now()
        try:
            return parse(value)
        except ValueError:
            raise ValidationError('Invalid pickup time')


class DropoffValidator(serializers.Serializer):
    address = AddressValidator(required=True)
    size = serializers.ChoiceField(
        choices=list(dict(PackageTypes.CHOICES).keys()), required=False)
    # instructions for courier
    notes = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    contact = ContactValidator(required=False)


class QuotesV1Validator(serializers.Serializer):
    pickup = serializers.CharField(required=False)
    dropoffs = serializers.ListField(
        child=serializers.CharField(), min_length=1, max_length=4)


class QuotesValidator(serializers.Serializer):
    pickup = PickupValidator(required=True)
    dropoffs = serializers.ListField(
        child=DropoffValidator(required=True), min_length=1, max_length=4
    )


class ServicePaymentValidator(serializers.Serializer):
    method = serializers.CharField(required=True)  # payment channel
    amount = serializers.FloatField(required=True)
    reference = serializers.CharField(required=True)

    def validate_method(self, value):
        payment_channels = dict(PaymentChannels.CHOICES).keys()
        if value not in payment_channels:
            raise ValidationError("Invalid payment channel")

        return value


class DeliveryValidator(serializers.Serializer):
    pickup = PickupValidator(required=True)
    dropoffs = serializers.ListField(
        child=DropoffValidator(required=True), min_length=1, max_length=4
    )
    quote = serializers.CharField(required=False)
    notes = serializers.CharField(required=False)
    payment = ServicePaymentValidator(required=True)
    collect_delivery_fee = serializers.NullBooleanField(required=False)


class WalletTopUpValidator(serializers.Serializer):
    amount = serializers.FloatField(required=True)
    reference = serializers.CharField(required=True)

    # TODO: validate reference originated from Paystack


class ChargeRefValidator(serializers.Serializer):
    amount = serializers.FloatField(required=True)
