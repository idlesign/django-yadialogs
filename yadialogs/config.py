from django.apps import AppConfig


class YadialogsConfig(AppConfig):
    """Конфигурация приложения."""

    name = 'yadialogs'
    verbose_name = 'Яндекс.Диалоги'

    def ready(self):
        """Инициализирует приложение."""
        from .toolbox import autodiscover_dialogs
        autodiscover_dialogs()
