from brockassemble.command import event


def test_basic_usage():
    result = event('@s', 'test_event')
    assert result == '/event entity @s test_event'


def test_exclude_slash():
    result = event('@s', 'test_event', False)
    assert result == 'event entity @s test_event'
