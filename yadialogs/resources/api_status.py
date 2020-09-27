from .base import Container


class Quota(Container):
    """Квота, выделанная под хранение данных."""

    key = 'quota'

    def __init__(self, raw: dict):
        super().__init__(raw)

        self.total = raw['total']
        """Всего байтов выделено."""

        self.used = raw['used']
        """Использовано байтов."""

        self.free = self.total - self.used
        """Доступно для использования байтов."""


class _SharedBase(Container):

    def __init__(self, raw: dict):
        super().__init__(raw)
        self.quota = Quota.from_raw(raw)


class Images(_SharedBase):

    key = 'images'


class Sounds(_SharedBase):
    """Для каждого аккаунта на Яндексе действует лимит на
    загрузку аудиофайлов — вы можете хранить на Диалогах
    не больше 1 ГБ файлов. Обратите внимание, лимит учитывает
    размер сжатых аудиофайлов, а не размер оригиналов.
    Диалоги конвертируют загруженные аудиофайлы в формат OPUS
    и обрезают их до 120 секунд — размер этих файлов и будет
    учитываться в лимите.

    """

    key = 'sounds'


class Status(Container):
    """Данные о доступных ресурсах."""

    def __init__(self, raw: dict):
        super().__init__(raw)

        self.images = Images.from_raw(raw)
        """Данные об изображениях."""

        self.sounds = Sounds.from_raw(raw)
        """Данные о звуковых файлах."""
