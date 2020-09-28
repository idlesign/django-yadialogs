from typing import List

from django.urls import path
from etc.toolbox import import_project_modules

from .settings import APP_MODULE_NAME
from .views import webhook


def autodiscover_dialogs():
    """Автоматически обнаруживает и регистрирует диалоги, распространяемые
    с подкленными Джанго-приложениями.

    """
    import_project_modules(APP_MODULE_NAME)


def get_yadialogs_urls() -> List:
    """Возвращает список URL-шаблонов yadialogs, который можно присовокупить
    к urlpatterns проекта:

    .. code-block:: python

        # Из urls.py:

        from yadialogs.toolbox import get_yadialogs_urls

        urlpatterns = urlpatterns + get_yadialogs_urls()  # Now attaching additional URLs.

    """
    urlpatterns = [
        path('<str:dialog>/', webhook, name='yadialogs_webhook'),
    ]

    return urlpatterns
