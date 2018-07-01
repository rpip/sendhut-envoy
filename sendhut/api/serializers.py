from rest_framework import serializers
from sendhut.accounts.models import User
from sendhut.addressbook.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('address', 'apt', 'location', 'photo', 'notes')


class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'addresses',
                  'username', 'phone', 'last_login', 'identity_verified')
