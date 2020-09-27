from .http import HttpClient
from .settings import API_KEY
from .resources.api_status import Status


class DialogsApi:

    url_base: str = 'https://dialogs.yandex.net/api/v1/'

    def __init__(self, *, token: str = ''):
        self.client = HttpClient(token=token or API_KEY)

    def get_status(self) -> Status:
        response = self.client.request(f'{self.url_base}status', json=True)
        return Status(response)
