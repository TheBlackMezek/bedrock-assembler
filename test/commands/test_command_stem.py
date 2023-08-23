from brockassemble.command import _command_stem


def test_no_optional_parameters():
    assert _command_stem('command') == '/command'


def test_with_selector():
    assert _command_stem('command', '@e') == '/command @e'


def test_with_no_slash():
    assert _command_stem('command', include_slash=False) == 'command'


def test_all_optional_parameters():
    assert _command_stem('command', '@e', False) == 'command @e'
