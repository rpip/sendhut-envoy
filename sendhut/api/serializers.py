# Atomic transactions https://github.com/getsentry/sentry/blob/master/src/sentry/api/endpoints/api_authorizations.py#L45
from sendhut.accounts.models import User
from sendhut.addressbook.models import Address, Contact
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
from .base import Serializer, register, serialize


@register(User)
class UserSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'id': obj.id,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'email': obj.email,
            'username': obj.get_username(),
            'last_login': obj.last_login,
            'identity_verified': obj.identity_verified,
            'is_active': obj.is_active,
            'date_joined': obj.date_joined,
            'addresses': serialize(obj.addresses.all())
        }


@register(Address)
class AddressSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'id': obj.id,
            'address': obj.address,
            'apt': obj.apt,
            'location': obj.location,
            'photo': obj.photo,
            'notes': obj.notes,
        }


@register(Contact)
class ContactSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'id': obj.id,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'phone': obj.phone,
            'email': obj.email,
            'address': serialize(obj.address)
        }


@register(DeliveryQuote)
class DeliveryQuoteSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'id': obj.id,
            'pickup': data.get('pickup'),
            'dropoffs': data.get('dropoffs'),
            'eta': obj.eta,
            'fee': obj.fee,
            'expires': obj.expires
        }


@register(Delivery)
class DeliverySerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'id': obj.id,
            'user': serialize(user),
            'pickup': serialize(obj.pickup),
            'dropoff': serialize(obj.dropoff),
            'delivered_at': obj.delivered_at,
            'distance': obj.distance,
            'quote': serialize(obj.quote),
            'tracking_url': obj.tracking_url,
            'notes': obj.notes,
            'courier': serialize(obj.courier),
            # TODO: check if fee differs from quote
            'fee': serialize(obj.fee)
        }


@register(Courier)
class CourierSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'id': obj.id,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'phone': obj.phone,
            'email': obj.email,
            'address': serialize(obj.address)
        }


@register(Pickup)
class PickupSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'id': obj.id,
            'address': serialize(obj.address),
            'notes': serialize(obj.notes),
            'contact': serialize(obj.contact)
        }


@register(Dropoff)
class DropoffSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'id': obj.id,
            'package_type': obj.package_type,
            'package_description': obj.package_description,
            'order_id': serialize(obj.order_id),
            'address': serialize(obj.address),
            'contact': serialize(obj.contact)
        }


@register(Zone)
class ZoneSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'name': obj.name,
            'code': obj.code,
            'region': obj.region,
            'timezone': obj.timezone,
            'location': obj.location
        }


@register(Batch)
class BatchSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'batch_id': obj.id,
            'deliveries': serialize(obj.deliveries.all())
        }


@register(Cancellation)
class CancellationSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'cancelled_by': obj.cancelled_by,
            'reason': obj.reason,
            'comment': obj.comment
        }
