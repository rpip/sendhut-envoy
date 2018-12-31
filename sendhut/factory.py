from datetime import datetime, timedelta
from random import choice
import glob

from django.core.files import File
from django.utils.text import slugify
from django.contrib.gis.geos import Point
from faker import Faker
from factory import (
    DjangoModelFactory, SubFactory,
    LazyFunction, lazy_attribute, Sequence, SelfAttribute
)

from sendhut.accounts.models import User
from sendhut.addressbook.models import Address, Contact, Image
from sendhut.partners.models import Partner
from sendhut.envoy.models import (
    Pickup, Dropoff, Zone, Courier,
    DeliveryQuote, Delivery, Batch
)
from sendhut.payments.models import Wallet, Transaction
from sendhut.payments import TransactionTypes

fake = Faker()

POINTS = [
    Point(6.456340, 3.416270),
    Point(6.445196, 3.539032)
]


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('phone',)

    first_name = lazy_attribute(lambda o: fake.first_name())
    last_name = lazy_attribute(lambda o: fake.last_name())
    username = Sequence(lambda n: '{}_{}'.format(fake.user_name(), n))
    email = lazy_attribute(lambda o: o.username + "@example.com")
    phone = lazy_attribute(lambda x: fake.phone_number())
    identity_verified = choice([True, False])


class ImageFactory(DjangoModelFactory):

    class Meta:
        model = Image

    def _random_image():
        images = glob.glob('./static/images/fixtures/*')
        return File(open(choice(images), 'rb'))

    image = LazyFunction(_random_image)


class AddressFactory(DjangoModelFactory):

    class Meta:
        model = Address

    # TODO(yao): build list of valid Lagos addresses
    address = lazy_attribute(lambda x: fake.address())
    apt = 'Q9'
    notes = lazy_attribute(lambda x: choice([None, fake.sentence()]))
    location = lazy_attribute(lambda x: choice(POINTS))
    photo = SubFactory(ImageFactory)


class ContactFactory(DjangoModelFactory):

    class Meta:
        model = Contact

    first_name = lazy_attribute(lambda o: fake.first_name())
    last_name = lazy_attribute(lambda o: fake.last_name())
    email = lazy_attribute(lambda o: fake.email())
    phone = lazy_attribute(lambda x: fake.phone_number())
    address = SubFactory(AddressFactory)


class PartnerFactory(DjangoModelFactory):

    class Meta:
        model = Partner

    first_name = lazy_attribute(lambda o: fake.first_name())
    last_name = lazy_attribute(lambda o: fake.last_name())
    email = lazy_attribute(lambda o: fake.email())
    phone = lazy_attribute(lambda x: fake.phone_number())
    address = SubFactory(AddressFactory)


class ZoneFactory(DjangoModelFactory):

    class Meta:
        model = Zone

    name = lazy_attribute(
        lambda o: '{} {}'.format(fake.city_prefix(), fake.city()))
    code = lazy_attribute(lambda o: slugify(o.name))
    location = lazy_attribute(lambda x: choice(POINTS))
    timezone = lazy_attribute(lambda x: fake.timezone())
    name = lazy_attribute(lambda o: fake.city())


class CourierFactory(DjangoModelFactory):

    class Meta:
        model = Courier

    first_name = lazy_attribute(lambda o: fake.first_name())
    last_name = lazy_attribute(lambda o: fake.last_name())
    phone = lazy_attribute(lambda x: fake.phone_number())
    location = lazy_attribute(lambda x: choice(POINTS))
    photo = SubFactory(ImageFactory)
    zone = SubFactory(ZoneFactory)
    partner = SubFactory(PartnerFactory)


class DeliveryQuoteFactory(DjangoModelFactory):

    class Meta:
        model = DeliveryQuote

    expires = lazy_attribute(lambda x: datetime.now() + timedelta(hours=1))
    eta = lazy_attribute(lambda x: datetime.now() + timedelta(minutes=25))
    fee = choice([1200, 900, 3500, 800, 400, 1400, 1650, 850])


class PickupFactory(DjangoModelFactory):

    class Meta:
        model = Pickup

    address = SubFactory(AddressFactory)
    notes = fake.sentence()
    contact = SubFactory(ContactFactory)


class DropoffFactory(DjangoModelFactory):

    class Meta:
        model = Dropoff

    package_description = lazy_attribute(lambda x: fake.sentence())
    address = SubFactory(AddressFactory)
    contact = SubFactory(ContactFactory)


class BatchFactory(DjangoModelFactory):

    class Meta:
        model = Batch


class DeliveryFactory(DjangoModelFactory):

    class Meta:
        model = Delivery

    user = SubFactory(UserFactory)
    pickup = SubFactory(PickupFactory)
    dropoff = SubFactory(DropoffFactory)
    quote = SubFactory(DeliveryQuoteFactory)
    tracking_url = lazy_attribute(lambda x: fake.uri())
    courier = SubFactory(CourierFactory)
    fee = choice([1200, 900, 3500, 800, 400, 1400, 1650, 850])
    batch = SubFactory(BatchFactory)


class WalletFactory(DjangoModelFactory):

    class Meta:
        model = Wallet

    user = SubFactory(UserFactory)


class TransactionFactory(DjangoModelFactory):

    class Meta:
        model = Transaction

    wallet = SubFactory(WalletFactory)
    amount = choice([5000, 50000, 6000, 8000, 10000, 20000])
    txn_type = lazy_attribute(lambda o: choice(dict(TransactionTypes.CHOICES).keys()))
