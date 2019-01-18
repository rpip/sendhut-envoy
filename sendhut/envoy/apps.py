from django.apps import AppConfig


class EnvoyConfig(AppConfig):
    name = 'sendhut.envoy'
    verbose_name = 'envoy'

    def ready(self):
        from . import signals
