# Atomic transactions https://github.com/getsentry/sentry/blob/master/src/sentry/api/endpoints/api_authorizations.py#L45
from django.contrib.gis.geos import Point
from djmoney.money import Money

from sendhut.accounts.models import User
from sendhut.addressbook.models import Address, Contact
from sendhut.payments.models import Wallet, Transaction
from sendhut.envoy.models import (
    DeliveryQuote,
    Delivery,
    Courier,
    Pickup,
    Dropoff,
    Zone,
    Batch,
    Cancellation,
    Partner
)
from .base import Serializer, register, serialize


@register(User)
class UserSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'id': obj.id,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'email': obj.get_email(),
            'username': obj.get_username(),
            'last_login': obj.last_login,
            'identity_verified': obj.identity_verified,
            'is_active': obj.is_active,
            'date_joined': obj.date_joined,
            'addresses': serialize(obj.addresses.all()),
            'wallet': serialize(obj.service_wallet)
        }


@register(Address)
class AddressSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'id': obj.id,
            'address': obj.address,
            'apt': obj.apt,
            'location': serialize(obj.location),
            # 'photo': obj.photo.thumb_sm().url if obj.photo else None,
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
        # TODO: add pickup and dropoff
        return {
            'id': obj.id,
            'eta': obj.eta,
            'fee': str(obj.fee),
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
            'fee': str(obj.fee),
            'status': obj.status
        }


@register(Courier)
class CourierSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'id': obj.id,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'phone': obj.phone,
            # TODO: use pregenerated thumbnails
            # 'photo': obj.photo.thumb_sm().url if obj.photo else None,
            'transport_type': serialize(obj.transport_type),
            'location': serialize(obj.location),
            'zone': serialize(obj.zone),
            'partner': serialize(obj.partner)
            # TODO: add email
            # 'email': obj.email,
        }


@register(Point)
class PointFieldSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        lat, lon = obj.coords
        return {
            'lat': lat,
            'lon': lon
        }


@register(Partner)
class PartnerSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'id': obj.id,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'phone': obj.phone,
            'email': obj.email,
            'address': obj.address
        }


@register(Pickup)
class PickupSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'id': obj.id,
            'address': serialize(obj.address),
            'pickup_time': serialize(obj.pickup_time),
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
            'location': serialize(obj.location)
        }


@register(Batch)
class BatchSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'batch_id': obj.id,
            'deliveries': serialize(list(obj.deliveries.all()))
        }


@register(Cancellation)
class CancellationSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'cancelled_by': obj.cancelled_by,
            'reason': obj.reason,
            'comment': obj.comment
        }


@register(Wallet)
class WalletSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'id': str(obj.id),
            'deposits': serialize(obj.get_deposits()),
            'total_deposits': str(obj.total_deposits),
            'withdrawals': str(obj.total_withdrawals),
            'balance': str(obj.balance),
            'is_empty': obj.is_empty
        }


@register(Transaction)
class TransactionSerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return {
            'amount': str(obj.amount),
            'type': obj.txn_type,
        }


@register(Money)
class MoneySerializer(Serializer):
    def serialize(self, obj, user, *args, **kwargs):
        return str(obj.amount)
