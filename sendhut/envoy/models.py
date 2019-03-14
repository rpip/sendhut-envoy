from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

from djmoney.models.fields import MoneyField
from safedelete.models import SOFT_DELETE_CASCADE

from sendhut.db import BaseModel, BaseQuerySet, BaseManager
from sendhut.addressbook.models import Address, Contact, Image
from sendhut.partners.models import Partner
from sendhut.utils import sane_repr
from sendhut.payments.models import Transaction
from sendhut.payments import TransactionTypes

from . import (
    TransportTypes, DeliveryStatus, PackageTypes,
    CancellationReasons, ZoneRegions
)


class Cancellation(BaseModel):

    ID_PREFIX = 'can'

    cancelled_by = models.ForeignKey(get_user_model())
    reason = models.CharField(
        max_length=100,
        choices=CancellationReasons.CHOICES)
    comment = models.CharField(max_length=152, null=True, blank=True)

    class Meta:
        db_table = 'cancellation'

    __repr__ = sane_repr('cancelled_by', 'reason')

    def __str__(self):
        return self.reason


class Courier(BaseModel):

    ID_PREFIX = 'cor'

    first_name = models.CharField(max_length=152)
    last_name = models.CharField(max_length=152)
    phone = models.CharField(max_length=30, unique=True)
    photo = models.ForeignKey(Image, related_name='courier', blank=True, null=True)
    transport_type = models.CharField(
        max_length=32, choices=TransportTypes.CHOICES,
        default=TransportTypes.BIKE
    )
    location = models.PointField(u"longitude/latitude", null=True, spatial_index=True, geography=True)
    zone = models.ForeignKey('Zone')
    partner = models.ForeignKey(Partner)
    # TODO(yao): add status field: onduty, offdduty

    class Meta:
        db_table = 'courier'

    __repr__ = sane_repr('city', 'postcode')

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Zone(BaseModel):

    ID_PREFIX = 'zon'

    name = models.CharField(max_length=42)
    code = models.CharField(max_length=32)
    region = models.CharField(max_length=32, choices=ZoneRegions.CHOICES)
    timezone = models.CharField(max_length=50, default='Africa/Lagos')
    location = models.PointField(null=True, spatial_index=True, geography=True)

    class Meta:
        db_table = 'zone'

    __repr__ = sane_repr('name', 'region')

    def __str__(self):
        return self.name


class DeliveryQuote(BaseModel):

    ID_PREFIX = 'dqt'

    # todo: add transport type & delivery mode: asap or scheduled
    expires = models.DateTimeField(null=True, blank=True)
    eta = models.DateTimeField(null=True, blank=True)
    fee = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency=settings.DEFAULT_CURRENCY,
        null=True, blank=True
    )

    class Meta:
        db_table = 'delivery_quote'

    __repr__ = sane_repr('fee')

    def __str__(self):
        return str(self.fee)


class ContactMixin:
    # TODO: return business profile if business account

    @property
    def contact_name(self):
        return "{0.first_name} {0.last_name}".format(self.contact)

    @property
    def contact_address(self):
        return self.address.address

    @property
    def contact_phone(self):
        return self.contact.phone


class Pickup(BaseModel, ContactMixin):

    ID_PREFIX = 'pkp'

    # TODO(yao): connect contact and address
    address = models.ForeignKey(Address)
    pickup_time = models.DateTimeField(null=True, blank=True)
    # instructions for courier
    notes = models.CharField(max_length=252, null=True, blank=True)
    contact = models.ForeignKey(Contact, null=True, blank=True)

    class Meta:
        db_table = 'pickup'

    __repr__ = sane_repr('address', 'contact')

    def __str__(self):
        return str(self.address)


class Dropoff(BaseModel, ContactMixin):

    ID_PREFIX = 'dpf'

    # TODO(yao): connect contact and address
    package_type = models.CharField(max_length=32, choices=PackageTypes.CHOICES)
    package_description = models.CharField(max_length=252, null=True, blank=True)
    order_id = models.CharField(max_length=32, null=True, blank=True)
    address = models.ForeignKey(Address)
    contact = models.ForeignKey(Contact)

    class Meta:
        db_table = 'dropoff'

    __repr__ = sane_repr('address', 'contact')

    def __str__(self):
        return str(self.address)


class DeliveryQuerySet(BaseQuerySet):
    """
    A specialized queryset for dealing with deliveries.
    """
    def ongoing(self):
        """Return ongoing deliveries"""
        return self.filter(status__in=[
            DeliveryStatus.PENDING, DeliveryStatus.ALMOST_PICKUP,
            DeliveryStatus.WAITING_AT_PICKUP, DeliveryStatus.PICKUP_COMPLETE,
            DeliveryStatus.DROPOFF, DeliveryStatus.ALMOST_DROPOFF,
            DeliveryStatus.WAITING_AT_DROPOFF
        ])

    def scheduled(self):
        """Return scheduled deliveries"""
        return self.filter(status=DeliveryStatus.SCHEDULED)

    def finished(self):
        """Return finished deliveries"""
        return self.filter(status=DeliveryStatus.DELIVERED)

    def expired(self):
        """Return finished deliveries"""
        return self.filter(status=DeliveryStatus.EXPIRED)

    def cancelled(self):
        """Return cancelled deliveries"""
        return self.filter(status=DeliveryStatus.CANCELLED)

    def incoming(self):
        """Return incoming deliveries"""
        return self.filter(status=DeliveryStatus.INCOMING)


class DeliveryManager(BaseManager):
    pass


class Delivery(BaseModel):

    ID_PREFIX = 'del'

    user = models.ForeignKey(get_user_model(), related_name='deliveries')
    status = models.CharField(
        max_length=32, choices=DeliveryStatus.CHOICES,
        default=DeliveryStatus.PENDING
    )
    pickup = models.ForeignKey(Pickup)
    dropoff = models.ForeignKey(Dropoff)
    picked_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    quote = models.ForeignKey(
        DeliveryQuote, related_name='delivery', null=True, blank=True)
    tracking_url = models.CharField(max_length=122, null=True, blank=True)
    notes = models.CharField(max_length=152, null=True, blank=True)
    courier = models.ForeignKey(Courier, related_name='deliveries', null=True, blank=True)
    fee = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency=settings.DEFAULT_CURRENCY,
        null=True, blank=True
    )
    batch = models.ForeignKey('Batch', related_name='deliveries', null=True, blank=True)

    objects = DeliveryManager.from_queryset(DeliveryQuerySet)()

    @property
    def duration(self):
        pass

    def for_user(user, status=None):
        if status:
            if hasattr(user.deliveries, status):
                return getattr(user.deliveries, status)()

            return Delivery.objects.filter(user=user, status=status)

        return Delivery.objects.filter(user=user)

    class Meta:
        db_table = 'delivery'

    __repr__ = sane_repr('pickup', 'dropoff', 'status')


class Batch(BaseModel):
    "A group of deliveries jobs requested together"

    ID_PREFIX = 'bat'

    def record_payment(self, amount, method, reference):
        return Transaction.make_payment(
            amount=amount,
            txn_type=TransactionTypes.PAYMENT,
            channel=method,
            reference=reference
        )

    class Meta:
        db_table = 'batch'

    __repr__ = sane_repr('address', 'contact')
