import logging
from typing import Optional, Union

from requests import Session, Response, RequestException

LOGGER = logging.getLogger(__name__)


class HttpClient:
    """Client to perform HTTP requests."""

    timeout: int = 10

    user_agent: str = ''

    def __init__(self, *, token: str):
        session = Session()
        session.headers.update({
            'Authorization': f'OAuth {token}',
        })
        self.session = session

    def request(
            self,
            url: str,
            *,
            data: dict = None,
            json: bool = None,
            silence_exceptions: bool = None,
            timeout: int = None,
            **kwargs
    ) -> Optional[Union[Response, dict]]:
        """

        :param url: URL to address
        :param data: Data to send to URL
        :param json: Send and receive data as JSON
        :param silence_exceptions: Do not raise exceptions
        :param timeout: Override timeout.
        :param kwargs:

        """
        LOGGER.debug(f'Fetching {url} ...')

        r_kwargs = {
            'timeout': timeout or self.timeout,
            **kwargs,
        }

        try:

            if data or r_kwargs.get('files'):

                if json:
                    r_kwargs['json'] = data
                else:
                    r_kwargs['data'] = data

                method = self.session.post

            else:
                method = self.session.get

            response = method(url, **r_kwargs)

        except RequestException as e:

            LOGGER.warning(f"Failed to get response from `{url}`: {e}")

            if silence_exceptions:
                return None

            raise

        else:

            if json:
                try:
                    response = response.json()

                except:
                    return {}

        return response
