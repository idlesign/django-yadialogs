from .base import Container


class User(Container):

    _key = 'user'

    def __init__(self, raw: dict):
        super().__init__(raw=raw)

        self.id = raw['user_id']
        """Идентификатор пользователя Яндекса, единый для всех приложений и устройств.
        Этот идентификатор уникален для пары «пользователь — навык»: в разных навыках
        значение свойства user_id для одного и того же пользователя будет различаться.

        """

        self.access_token = raw['access_token']
        """Токен для OAuth-авторизации, который также передается в заголовке Authorization
        для навыков с настроенной связкой аккаунтов.

        """


class Application(Container):

    _key = 'application'

    def __init__(self, raw: dict):
        super().__init__(raw=raw)

        self.id = raw['application_id']
        """Идентификатор экземпляра приложения, в котором пользователь
        общается с Алисой, максимум 64 символа. Например, даже если пользователь авторизован
        с одним и тем же аккаунтом в приложениях Яндекс для Android и iOS,
        Яндекс.Диалоги присвоят отдельный application_id каждому из этих приложений.
        Этот идентификатор уникален для пары «приложение — навык»: в разных навыках значение
        свойства application_id для одного и того же пользователя будет различаться.

        """


class Session(Container):
    """Сессия — это период относительно непрерывного взаимодействия пользователя с навыком."""

    _key = 'session'

    def __init__(self, raw):
        super().__init__(raw=raw)

        self.id = raw['session_id']
        """Уникальный идентификатор сессии, максимум 64 символов."""

        self.message_id = raw['message_id']
        """Идентификатор сообщения в рамках сессии, максимум 8 символов.
        Инкрементируется с каждым следующим запросом.

        """

        self.skill_id = raw['skill_id']
        """Идентификатор вызываемого навыка, присвоенный при создании."""

        self.skill = None  # todo

        self.user = User.from_raw(raw)
        """Атрибуты пользователя Яндекса, который взаимодействует с навыком.
        Если пользователь не авторизован в приложении, свойства user в запросе не будет.

        """

        self.application = Application.from_raw(raw)
        """Данные о приложении, с помощью которого пользователь взаимодействует с навыком."""

        self.new = raw['new']
        """Признак новой сессии. Возможные значения:
        true — пользователь начинает новый разговор с навыком;
        false — запрос отправлен в рамках уже начатого разговора.
        
        """


class Meta(Container):
    """Информация об устройстве, с помощью которого пользователь разговаривает с Алисой."""

    _key = 'meta'

    def __init__(self, raw: dict):
        super().__init__(raw=raw)
        self.locale = raw['locale']
        self.timezone = raw['timezone']


class Request(Container):
    """Данные, полученные от пользователя."""

    _key = 'request'


class Callback(Container):

    def __init__(self, raw):
        super().__init__(raw=raw)

        self.meta = Meta.from_raw(raw)
        """Информация об устройстве, с помощью которого пользователь разговаривает с Алисой."""

        self.request = Request.from_raw(raw)
        """Данные, полученные от пользователя."""

        self.session = Session.from_raw(raw)
        """Данные о сессии."""

        self.version = raw['version']
        """Версия протокола. """
