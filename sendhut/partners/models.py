from django.db import models

from sendhut.db import BaseModel
from . import DeliveryVolumes


class Partner(BaseModel):

    ID_PREFIX = 'par'

    first_name = models.CharField(max_length=152)
    last_name = models.CharField(max_length=152)
    email = models.EmailField(max_length=42, unique=True)
    phone = models.CharField(max_length=30, unique=True)
    address = models.CharField(
        max_length=80, unique=True, blank=True, null=True)

    class Meta:
        db_table = 'partner'


class Merchant(BaseModel):

    ID_PREFIX = 'mer'

    class Meta:
        db_table = "merchant"

    name = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30, null=True, blank=True, unique=True)
    email = models.EmailField(max_length=70, null=True, blank=True, unique=True)
    has_fleets = models.BooleanField(default=False)
    delivery_volume = models.CharField(
        choices=DeliveryVolumes.CHOICES, blank=True, null=True, max_length=50)
