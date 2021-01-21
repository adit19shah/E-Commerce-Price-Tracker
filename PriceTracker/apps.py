from django.apps import AppConfig
from django.conf import settings

class PricetrackerConfig(AppConfig):
    name = 'PriceTracker'

    def ready(self):
        from . import scheduler
        if settings.SCHEDULER_AUTOSTART:
            scheduler.start()
