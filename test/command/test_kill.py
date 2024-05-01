from brockassemble.command import kill


def test_basic_usage():
    result = kill('@p')
    assert result == '/kill @p'


def test_exclude_slash():
    result = kill('@p', False)
    assert result == 'kill @p'
