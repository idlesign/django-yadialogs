from typing import Dict, Type, Optional


class Dialog:
    """Base for dialogs."""

    id: str = ''
    """Identifier given to a dialog after its registration."""

    alias: str = ''
    """Convenience alias for a dialog."""

    dialogs: Dict[str, Dict[str, Type['Dialog']]] = {
        'alias': {},
        'id': {},
    }
    """All registered dialogs."""

    def __init__(self, request: dict):
        """
        :param request: Data from Dialogs server.

        """
        self.request = request

    def __init_subclass__(cls):

        super().__init_subclass__()

        if cls.id and cls.alias:
            cls.dialogs['alias'][cls.alias] = cls
            cls.dialogs['id'][cls.id] = cls

    @classmethod
    def handle_request(cls, request: dict) -> dict:
        """Handles request from Dialogs server.

        :param request: Data from server.

        """
        response = {}

        dialog = cls(request)
        dialog.process()

        return response

    @classmethod
    def get(cls, dialog: str, by_id: bool = False) -> Optional[Type['Dialog']]:
        """Get dialog type by its alias or id.

        :param dialog: Dialog alias or id.

        :param by_id: Get by id instead of an alias.

        """
        return cls.dialogs['id' if by_id else 'alias'].get(dialog)

    def process(self) -> dict:
        """Should implement server request processing and return a response."""
        raise NotImplementedError
