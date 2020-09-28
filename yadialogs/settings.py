from django.conf import settings

try:  # pragma: nocover
    from envbox import get_environment
    environ = get_environment()

except ImportError:
    from os import environ


APP_MODULE_NAME = getattr(settings, 'YADIALOGS_APP_MODULE_NAME', 'dialogs')
"""Имя модуля, расположанного в приложениях, в которых треубется искать диалоги."""

API_KEY = getattr(settings, 'YADIALOG_API_KEY', environ.get('YADIALOG_API_KEY', ''))
"""Ключ OAuth для доступа к HTTP API Диалогов."""

API_TIMEOUT = getattr(settings, 'YADIALOG_API_TIMEOUT', environ.get('YADIALOG_API_TIMEOUT', 5))
"""Таймаут для взаимодествия с HTTP API Диалогов."""
