from django.apps import AppConfig


class DictionaryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dictionary"
    verbose_name = "Dictionary"

    def ready(self):
        from . import signals