from django.conf import settings

try:  # pragma: nocover
    from envbox import get_environment
    environ = get_environment()

except ImportError:
    from os import environ


APP_MODULE_NAME = getattr(settings, 'YADIALOGS_APP_MODULE_NAME', 'dialogs')
"""Module name to search applications for dialogs in."""

API_KEY = getattr(settings, 'YADIALOG_API_KEY', environ.get('YADIALOG_API_KEY', ''))
"""OAuth key to access dialogs API."""
