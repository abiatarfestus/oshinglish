from django.apps import AppConfig


class DictionaryConfig(AppConfig):
    name = "dictionary"
    verbose_name = "Dictionary"

    def ready(self):
        import dictionary.signals
