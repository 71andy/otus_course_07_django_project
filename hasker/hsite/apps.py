from django.apps import AppConfig


class HsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hsite'

    def ready(self):
        import hsite.signals
