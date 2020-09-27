from yadialogs.toolbox import Dialog


class DialogOne(Dialog):

    id = '1-1'
    alias = 'dione'

    def process(self) -> dict:
        return {}


class DialogTwo(Dialog):

    id = '2-2-2'
    alias = 'ditwo'


class DialogBogus(Dialog):

    id = ''
    alias = 'bogus'
