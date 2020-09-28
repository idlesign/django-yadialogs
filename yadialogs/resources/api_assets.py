from datetime import datetime

from django.utils.dateparse import parse_datetime

from .base import Container


class _Asset(Container):

    def __init__(self, *, dialog_id: str, raw: dict):
        super().__init__(raw=raw)

        self.dialog_id: str = dialog_id
        """Идентификатор диалога."""

        self.id: str = raw['id']
        """Идентификатор ресурса."""

        self.size: int = raw['size'] or 0
        """Размер ресурса, байтов."""

        self.uploaded: datetime = parse_datetime(raw['createdAt'])
        """Дата и время загрузки ресурса."""

    def __str__(self) -> str:
        return self.id


class Image(_Asset):
    """Изображение."""

    def __init__(self, *, dialog_id: str, raw: dict):
        super().__init__(dialog_id=dialog_id, raw=raw)

        self.orig_url: str = raw.get('origUrl') or ''
        """URL изображения (если оно было загружено используя URL)."""


class Sound(_Asset):
    """Звукозапись."""

    def __init__(self, *, dialog_id: str, raw: dict):
        super().__init__(dialog_id=dialog_id, raw=raw)

        self.orig_name: str = raw['originalName']
        """Оригинальное имя файла."""

        self.is_processed: bool = raw['isProcessed']
        """Флаг законченности обработки."""

        self.error: str = raw['error'] or ''
        """Описание ошибки обработки."""
