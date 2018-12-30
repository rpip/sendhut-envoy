from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from sendhut.payments.models import Wallet


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def init_new_user(sender, instance, signal, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
        Token.objects.create(user=instance)
