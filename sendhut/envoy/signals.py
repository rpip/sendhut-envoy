from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Delivery
from sendhut import notifications


CHANNEL = '#orders'


@receiver(post_save, sender=Delivery)
def init_new_user(sender, instance, signal, created, **kwargs):
    if created:
        # save to Airtable & post slack alert
        message = "New delivery request: {}".format(
            instance.get_absolute_url())
        notifications.post_to_slack(message, CHANNEL)
