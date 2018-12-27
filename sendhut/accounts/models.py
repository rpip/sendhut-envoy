from django.contrib.auth.models import AbstractUser
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

    def get_contacts(self):
        def _extract_contacts(delivery):
            return [delivery.pickup.contact] + \
                [x.dropoff.contact for x in delivery.batch.deliveries.all()]

        contacts = [_extract_contacts(d) for d in self.deliveries.all()]
        return sum(contacts, [])

    __repr__ = sane_repr('id')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def contact_details(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.default_address
        }

    @property
    def default_address(self):
        return self.addresses.first()

    class Meta:
        db_table = 'user'
