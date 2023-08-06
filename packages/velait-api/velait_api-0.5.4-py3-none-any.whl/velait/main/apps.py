from django.apps import AppConfig


class VelaitConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "velait"

    def ready(self):
        import velait.main.signals
