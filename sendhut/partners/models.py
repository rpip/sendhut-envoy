from django.db import models

from sendhut.db import BaseModel


class Partner(BaseModel):

    ID_PREFIX = 'par'

    first_name = models.CharField(max_length=152)
    last_name = models.CharField(max_length=152)
    email = models.EmailField(max_length=42, unique=True)
    phone = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=80, unique=True)

    class Meta:
        db_table = 'partner'
