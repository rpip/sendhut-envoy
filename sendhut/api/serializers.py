# Atomic transactions https://github.com/getsentry/sentry/blob/master/src/sentry/api/endpoints/api_authorizations.py#L45
from sendhut.accounts.models import User
from sendhut.addressbook.models import Address
from sendhut.envoy.models import (
    DeliveryQuote,
    Delivery,
    Courier,
    Pickup,
    Dropoff,
    Zone,
    Batch,
    Cancellation
)
from .base import register, Serializer


@register(User)
class UserSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {}


@register(Address)
class AddressSerializer(Serializer):
    pass


@register(DeliveryQuote)
class DeliveryQuoteSerializer(Serializer):
    pass


@register(Delivery)
class DeliverySerializer(Serializer):
    pass


@register(Courier)
class CourierSerializer(Serializer):
    pass


@register(Pickup)
class PickupSerializer(Serializer):
    pass


@register(Dropoff)
class DropoffSerializer(Serializer):
    pass


@register(Zone)
class ZoneSerializer(Serializer):
    pass


@register(Batch)
class BatchSerializer(Serializer):
    pass


@register(Cancellation)
class CancellationSerializer(Serializer):
    pass
