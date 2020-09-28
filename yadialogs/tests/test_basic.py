from yadialogs.toolbox import Dialog


def test_basic():
    assert Dialog.dialogs['alias']

    dialog = Dialog.get('dione')
    assert dialog
    assert Dialog.get('1-1', by_id=True) is dialog

    # No id for this dialog
    assert Dialog.get('bogus') is None
