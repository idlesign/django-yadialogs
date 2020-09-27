from typing import List

from django.urls import path
from etc.toolbox import import_project_modules

from .settings import APP_MODULE_NAME
from .views import webhook


def autodiscover_dialogs():
    """Autodiscover and register dialogs from pluggable apps."""
    import_project_modules(APP_MODULE_NAME)


def get_yadialogs_urls() -> List:
    """Returns yadialogs urlpatterns, that can be attached to urlpatterns of a project:

    .. code-block:: python

        # Example from urls.py.

        from yadialogs.toolbox import get_yadialogs_urls

        urlpatterns = urlpatterns + get_yadialogs_urls()  # Now attaching additional URLs.

    """
    urlpatterns = [
        path('<str:dialog>/', webhook, name='yadialogs_webhook'),
    ]

    return urlpatterns
