from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    name = 'sendhut.payments'
    verbose_name = "payments"

    # def ready(self):
    #     from . import signals
