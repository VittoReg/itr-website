from django.apps import AppConfig

class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    # ADD THIS METHOD
    def ready(self):
        import website.signals