from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class YadialogsConfig(AppConfig):
    """Application configuration."""

    name = 'yadialogs'
    verbose_name = _('Yandex Dialogs')

    def ready(self):
        """Application initialization."""
        from .toolbox import autodiscover_dialogs
        autodiscover_dialogs()
