from django.contrib.auth.models import AbstractUser
from django.db import models

from sendhut.utils import sane_repr
from sendhut.db import BaseModel


class User(AbstractUser, BaseModel):

    ID_PREFIX = 'usr'

    phone = models.CharField(max_length=20, unique=True)
    last_login = models.DateTimeField(null=True, blank=True)
    identity_verified = models.BooleanField(default=False)

    __repr__ = sane_repr('id')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        db_table = 'user'
