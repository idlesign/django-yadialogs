
class Container:

    _key: str = ''

    def __init__(self, *, raw: dict):
        self._raw = raw

    @classmethod
    def from_raw(cls, raw: dict):
        data = raw.get(cls._key)

        if data is None:
            return None

        return cls(raw=data)
