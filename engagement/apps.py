from django.apps import AppConfig
from django.apps import AppConfig

class EngagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'engagement'

    def ready(self):
        # Import signals here so they are loaded
        import engagement.signals


