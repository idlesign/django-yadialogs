
class Container:

    key: str = ''

    def __init__(self, raw: dict):
        self.raw = raw

    @classmethod
    def from_raw(cls, raw: dict):
        data = raw.get(cls.key)

        if data is None:
            return None

        return cls(data)
