from pathlib import Path
from typing import Callable, Union

from requests import Session

from . import VERSION_STR
from .settings import API_TIMEOUT


class HttpClient:
    """Клиент для соверщения HTTP запросов."""

    timeout: int = API_TIMEOUT

    user_agent: str = ''

    def __init__(self, *, token: str):
        session = Session()
        session.headers.update({
            'Authorization': f'OAuth {token}',
            'User-Agent': f'django-yadialogs/{VERSION_STR}',
        })
        self.session = session

    def _request(self, *, method: Callable, url, **kwargs) -> dict:
        response = method(url, **{'timeout': self.timeout, **kwargs})
        response.raise_for_status()
        data = response.json()
        return data

    def delete(self, url: str) -> dict:
        return self._request(method=self.session.delete, url=url)

    def upload(self, url: str, *, fpath: Union[Path, str]) -> dict:
        return self._request(method=self.session.post, url=url, files={'file': open(f'{fpath}', 'rb')})

    def get(self, url: str) -> dict:
        return self._request(method=self.session.get, url=url)
