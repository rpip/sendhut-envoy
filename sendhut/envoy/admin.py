# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Cancellation, Courier, Zone, DeliveryQuote, Pickup, Dropoff, Batch, Delivery


@admin.register(Cancellation)
class CancellationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
        'deleted',
        'metadata',
        'cancelled_by',
        'reason',
        'comment',
    )
    list_filter = ('created', 'updated', 'deleted', 'cancelled_by')


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
        'deleted',
        'metadata',
        'first_name',
        'last_name',
        'phone',
        'photo',
        'transport_type',
        'location',
        'zone',
        'partner',
    )
    list_filter = ('created', 'updated', 'deleted')


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
        'deleted',
        'metadata',
        'name',
        'code',
        'region',
        'timezone',
        'location',
    )
    list_filter = ('created', 'updated', 'deleted')
    search_fields = ('name',)


@admin.register(DeliveryQuote)
class DeliveryQuoteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
        'deleted',
        'metadata',
        'expires',
        'eta',
        'fee_currency',
        'fee',
    )
    list_filter = ('created', 'updated', 'deleted', 'expires', 'eta')


@admin.register(Pickup)
class PickupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
        'deleted',
        'metadata',
        'address',
        'notes',
        'contact',
    )
    list_filter = ('created', 'updated', 'deleted')


@admin.register(Dropoff)
class DropoffAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
        'deleted',
        'metadata',
        'package_type',
        'package_description',
        'order_id',
        'address',
        'contact',
    )
    list_filter = ('created', 'updated', 'deleted')


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'updated', 'deleted', 'metadata')
    list_filter = ('created', 'updated', 'deleted')


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
        'user',
        'get_status',
        'pickup',
        'dropoff',
        'picked_at',
        'delivered_at',
        'distance',
        'quote',
        'tracking_url',
        'notes',
        'courier',
        'batch',
    )
    list_filter = (
        'created',
        'updated',
        'deleted',
        'picked_at',
        'delivered_at',
    )
    exclude = ('fee', 'fee_currency')

    def get_status(self, obj):
        return obj.status

    get_status.allow_tags = True
    get_status.short_description = 'Status'
