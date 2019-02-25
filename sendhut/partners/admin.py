from django.contrib import admin

from sendhut.db import BaseModelAdmin
from .models import Merchant


@admin.register(Merchant)
class MerchantAdmin(BaseModelAdmin):
    list_display = (
        'id',
        'name',
        'business_name',
        'phone',
        'email',
        'created',
    )
    list_filter = (
        'delivery_volume',
        'created',
    )
