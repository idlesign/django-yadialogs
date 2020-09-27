from yadialogs.toolbox import Dialog
from yadialogs.api import DialogsApi


def test_basic():
    assert Dialog.dialogs['alias']

    dialog = Dialog.get('dione')
    assert dialog
    assert Dialog.get('1-1', by_id=True) is dialog

    # No id for this dialog
    assert Dialog.get('bogus') is None


def test_api_status(response_mock):

    bypass = False

    api = DialogsApi()

    with response_mock(
            'GET https://dialogs.yandex.net/api/v1/status -> 200: '
            '{"images":{"quota":{"total":104857600,"used":120}},"sounds":{"quota":{"total":1073741824,"used":1234567}}}',
            bypass=bypass
    ):
        status = api.get_status()
        assert status.sounds.quota.total == 1073741824
        assert status.sounds.quota.free == 1072507257
        assert status.sounds.quota.used == 1234567

        assert status.images.quota.total == 104857600
        assert status.images.quota.free == 104857480
        assert status.images.quota.used == 120
