from pathlib import Path
from typing import Union, Type, List

from .http import HttpClient
from .resources.api_assets import Image, Sound
from .resources.api_status import Status, ImagesInfo, SoundsInfo
from .settings import API_KEY


class _ApiRealm:

    _name: str = ''
    _asset_cls: Union[Type[Image], Type[Sound]]

    def __init__(self, *, api: 'DialogsApi'):
        self._api = api

    def _get_url_base(self, *, dialog_id: str) -> str:
        return f'{self._api._url_base}/skills/{dialog_id}/{self._name}'

    def get_info(self) -> Union[ImagesInfo, SoundsInfo]:
        """Возвращает информацию о хранилище ресурсов (изображений или звукозаписей)."""
        return getattr(self._api.get_status(), self._name)

    def upload(self, *, dialog_id: str, fpath: Union[Path, str]):
        """Загружает указанный файл ресурса (изображения или звукозаписи.)

        :param dialog_id: Идентификатор диалога.
        :param fpath: Путь до файла.

        """
        response = self._api._client.upload(self._get_url_base(dialog_id=dialog_id), fpath=fpath)
        return self._asset_cls(dialog_id=dialog_id, raw=response[self._name.rstrip('s')])

    def list(self, *, dialog_id: str) -> Union[List[Image], List[Sound]]:
        """Возвращает список с объектами ресурсов (изображений или звукозаписей).

        :param dialog_id: Идентификатор диалога.

        """
        response = self._api._client.get(self._get_url_base(dialog_id=dialog_id))
        asset_cls = self._asset_cls
        return [asset_cls(dialog_id=dialog_id, raw=asset) for asset in response[self._name]]

    def delete(self, *, asset: Union[str, Image, Sound], dialog_id: str = '') -> bool:
        """Удаляет указанный ресурс.

        :param asset: Объект ресурса или его идентификатор.
        :param dialog_id: Идентификатор диалога.

        """
        dialog_id = dialog_id or getattr(asset, 'dialog_id')
        return self._api._client.delete(f'{self._get_url_base(dialog_id=dialog_id)}/{asset}')['result'] == 'ok'


class _ImagesApi(_ApiRealm):
    """Интерфейс для доступа к данным хранилища изображений."""

    _name: str = 'images'
    _asset_cls: Type[Image] = Image


class _SoundsApi(_ApiRealm):
    """Интерфейс для доступа к данным хранилища звукозаписей."""

    _name: str = 'sounds'
    _asset_cls: Type[Sound] = Sound

    def get(self, *, dialog_id: str, asset_id: str) -> Union[Image, Sound]:
        """Возвращает объект ресурса с информацией о нём.

        :param dialog_id: Идентификатор диалога.
        :param asset_id: Идентификатор ресурса.

        """
        response = self._api._client.get(f'{self._get_url_base(dialog_id=dialog_id)}/{asset_id}')
        return self._asset_cls(dialog_id=dialog_id, raw=response[self._name.rstrip('s')])


class DialogsApi:
    """Предоставляет интерфейс для взаимодействия с API Диалогов."""

    _url_base: str = 'https://dialogs.yandex.net/api/v1'

    def __init__(self, *, token: str = ''):
        self._client = HttpClient(token=token or API_KEY)

        self.images = _ImagesApi(api=self)
        """Интерфейс для доступа к хранилищу изображений."""

        self.sounds = _SoundsApi(api=self)
        """Интерфейс для доступа к хранилищу звукозаписей."""

    def get_status(self) -> Status:
        """Возвращает объект со статусной информацией."""
        response = self._client.get(f'{self._url_base}/status')
        return Status(response)
