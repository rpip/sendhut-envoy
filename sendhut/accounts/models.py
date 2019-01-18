from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

from sendhut.utils import sane_repr
from sendhut.db import BaseModel


class User(AbstractUser, BaseModel):

    ID_PREFIX = 'usr'

    phone = models.CharField(max_length=20, unique=True)
    last_login = models.DateTimeField(null=True, blank=True)
    identity_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)

    def get_username(self):
        return self.phone

    def get_email(self):
        return self.email or "{}@sendhut.com".format(self.phone)

    def get_contacts(self):
        def _extract_contacts(delivery):
            return [delivery.pickup.contact] + \
                [x.dropoff.contact for x in delivery.batch.deliveries.all()]

        contacts = [_extract_contacts(d) for d in self.deliveries.all()]
        return sum(contacts, [])

    @property
    def contact_details(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.get_email(),
            'phone': self.phone,
            'address': self.default_address
        }

    @property
    def default_address(self):
        return self.addresses.first()

    @property
    def service_wallet(self):
        return self.wallets.get_service_wallet(self)

    @property
    def country(self):
        return settings.SUPPORTED_COUNTRIES[self.phone[:4]]

    def build_profile_context(self):
        """
        App-wide context for this user:
        - is_active?
        - locale: country, language
        - business_profile
        - whats_new
        - fav_addresses
        - refresh_schedules
        """
        return {
            'locale': dict(country=self.get_country())
        }
        pass

    class Meta:
        db_table = 'user'

    __repr__ = sane_repr('id')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
