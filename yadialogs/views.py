import logging
from django.http import (
    HttpRequest, JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseBadRequest,
    HttpResponseServerError)
from json import loads

from .dialog import Dialog

LOG = logging.getLogger(__name__)


def webhook(request: HttpRequest, dialog: str) -> HttpResponse:
    """Handles requests from Yandex Dialogs server.

    :param request:
    :param dialog: Dialog alias.

    """
    if not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    dialog_cls = Dialog.get(dialog)

    if dialog_cls is None:
        return HttpResponseNotFound(f'Dialog {dialog} is not registered.'.encode())

    try:
        data = loads(request.body)

    except Exception:
        return HttpResponseBadRequest()

    try:
        processed = dialog_cls.handle_request(data)

    except Exception:
        msg = f'Dialog {dialog} failure.'
        LOG.exception(msg)
        return HttpResponseServerError(msg.encode())

    return JsonResponse(processed)
