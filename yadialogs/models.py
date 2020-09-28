from django.core.files.storage import FileSystemStorage
from django.db import models


TmpStorage = FileSystemStorage(location='/tmp')


def get_upload(instance: 'Asset', filename):
    return 'some'


class Asset(models.Model):
    """Ресурс. Базовая модель."""

    _api_realm: str = ''

    class Statuses(models.IntegerChoices):
        """Статусы ресурсов."""

        UPLOADED = 1, 'Загружен'
        ERROR = 2, 'Ошибка'

    rid = models.CharField('ID', max_length=50, help_text='Идентификатор ресурса')

    dt_uploaded = models.DateTimeField('Загружен', db_column='db_upl')

    status = models.IntegerField('Статус', choices=Statuses.choices, default=Statuses.UPLOADED)
    status_hint = models.TextField('Подсказка', help_text='Подсказка для состояния.')

    dialog_alias = models.CharField(
        'Диалог', max_length=36, db_index=True, db_column='dalias',
        help_text='Псевдоним диалога')

    alias = models.CharField(
        'Псевдоним', max_length=50, null=True, default=None, unique=True,
        help_text='Краткое имя для удобной адресации ресурса')

    group = models.UUIDField(
        'Группа', null=True, default=None, db_column='grp',
        help_text='Идентификатор, объединяющий группу ресурсов')

    file = models.FileField(
        'Файл', upload_to=get_upload, storage=TmpStorage)

    size = models.IntegerField('Размер файла')

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.rid} [{self.alias}]'


class Image(Asset):
    """Изображение."""

    _api_realm: str = 'images'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Sound(Asset):
    """Звукозапись."""

    _api_realm: str = 'sounds'

    class Meta:
        verbose_name = 'Звук'
        verbose_name_plural = 'Звуки'
