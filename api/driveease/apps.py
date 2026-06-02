from django.apps import AppConfig


class DriveeaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'driveease'

    def ready(self):
        import driveease.signals