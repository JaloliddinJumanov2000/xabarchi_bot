from django.apps import AppConfig


class AppMainConfig(AppConfig):  # ⚠️ nomini o'zgartirdik
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        import app.signals
