from django.db.models.signals import post_save
from django.dispatch import receiver

from .core import AirTableManager
from .models import Delivery
from sendhut import notifications

CHANNEL = '#orders'

EnvoyAirtable = AirTableManager()


@receiver(post_save, sender=Delivery)
def incoming_delivery(sender, instance, signal, created, **kwargs):
    if created:
        # save to Airtable
        EnvoyAirtable.create_task(instance)
        # post slack alert
        message = "New delivery request: {}".format(
            instance.get_admin_url())
        notifications.post_to_slack(message, CHANNEL)
