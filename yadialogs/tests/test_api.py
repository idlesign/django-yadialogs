from yadialogs.api import DialogsApi

# todo datafixtures img sound
# список может быть без картинок
# card.button/  text / payload|url
# размеры изображений
# 388x172 582x258 776x344 1164x516 1358x602 1552x688

DIALOG_ID = '0c3dab01-4b05-4ea7-807c-dd18f34311ac'


def test_status(response_mock):

    bypass_mock = False

    api = DialogsApi()

    with response_mock(
        'GET https://dialogs.yandex.net/api/v1/status -> 200: '
        '{"images":{"quota":{"total":104857600,"used":120}},"sounds":{"quota":{"total":1073741824,"used":1234567}}}',
        bypass=bypass_mock
    ):
        status = api.get_status()
        assert status.sounds.quota.total == 1073741824
        assert status.sounds.quota.free == 1072507257
        assert status.sounds.quota.used == 1234567

        assert status.images.quota.total == 104857600
        assert status.images.quota.free == 104857480
        assert status.images.quota.used == 120


def test_images(response_mock, datafix_dir):

    bypass_mock = False

    api = DialogsApi()

    img_id = '000000/0116eeaf02d77a7331d6'
    img_fpath = datafix_dir / 'test.bmp'

    req = [
        'GET https://dialogs.yandex.net/api/v1/status -> 200:'
        '{"images":{"quota":{"total":104857600,"used":120}},"sounds":{"quota":{"total":1073741824,"used":1234567}}}',

        f'GET https://dialogs.yandex.net/api/v1/skills/{DIALOG_ID}/images -> 200:'
        '{"images":[],"total":0}',

        f'POST https://dialogs.yandex.net/api/v1/skills/{DIALOG_ID}/images -> 201:'
        '{"image":{"id":"%s","size":45651,"createdAt":"2020-09-26T04:30:43.085Z"}}' % img_id,
        
        f'GET https://dialogs.yandex.net/api/v1/skills/{DIALOG_ID}/images -> 200:'
        '{"images":[{"id":"%s","origUrl":null,"size":45651,"createdAt":"2020-09-26T04:19:20.404Z"}],"total":1}' % img_id,

        f'DELETE https://dialogs.yandex.net/api/v1/skills/{DIALOG_ID}/images/{img_id} -> 200:'
        '{"result":"ok"}',
    ]

    with response_mock(req, bypass=bypass_mock):
        api_images = api.images

        info = api_images.get_info()
        assert info.quota.total == 104857600

        images = api_images.list(dialog_id=DIALOG_ID)
        assert not images

        image = api_images.upload(dialog_id=DIALOG_ID, fpath=img_fpath)
        assert image.id

        images = api_images.list(dialog_id=DIALOG_ID)
        assert images[0].id

        assert api_images.delete(asset=image)


def test_sounds(response_mock, datafix_dir):

    bypass_mock = False

    api = DialogsApi()

    sound_id = '000000/0116eeaf02d77a7331d6'
    sound_fpath = datafix_dir / 'test.mp3'

    req = [
        'GET https://dialogs.yandex.net/api/v1/status -> 200:'
        '{"sounds":{"quota":{"total":104857600,"used":120}},"sounds":{"quota":{"total":1073741824,"used":1234567}}}',

        f'GET https://dialogs.yandex.net/api/v1/skills/{DIALOG_ID}/sounds -> 200:'
        '{"sounds":[],"total":0}',

        f'POST https://dialogs.yandex.net/api/v1/skills/{DIALOG_ID}/sounds -> 201:'
        '{"sound":{"id":"%s","skillId":"%s","size":null,"originalName":"test.png",'
        '"createdAt":"2020-09-26T04:55:13.331Z","isProcessed":false,"error":null}}' % (sound_id, DIALOG_ID),

        f'GET https://dialogs.yandex.net/api/v1/skills/{DIALOG_ID}/sounds/{sound_id} -> 200:'
        '{"sound":{"id":"%s","skillId":"%s","size":null,"originalName":"test.png",'
        '"createdAt":"2020-09-26T04:55:13.331Z","isProcessed":true,"error":null}}' % (sound_id, DIALOG_ID),

        f'GET https://dialogs.yandex.net/api/v1/skills/{DIALOG_ID}/sounds -> 200:'
        '{"sounds":[{"id":"%s","skillId":"%s","size":null,"originalName":"test.mp3",'
        '"createdAt":"2020-09-26T05:03:14.421Z","isProcessed":false,"error":"Unable to process file"}],"total":1}' %
        (sound_id, DIALOG_ID),

        f'DELETE https://dialogs.yandex.net/api/v1/skills/{DIALOG_ID}/sounds/{sound_id} -> 200:'
        '{"result":"ok"}',
    ]

    with response_mock(req, bypass=bypass_mock):
        api_sounds = api.sounds

        info = api_sounds.get_info()
        assert info.quota.total == 1073741824

        sounds = api_sounds.list(dialog_id=DIALOG_ID)
        assert not sounds

        sound = api_sounds.upload(dialog_id=DIALOG_ID, fpath=sound_fpath)
        assert sound.id

        sound2 = api_sounds.get(dialog_id=DIALOG_ID, asset_id=sound.id)
        assert sound2.id == sound.id

        sounds = api_sounds.list(dialog_id=DIALOG_ID)
        assert sounds[0].id

        assert api_sounds.delete(asset=sound)
