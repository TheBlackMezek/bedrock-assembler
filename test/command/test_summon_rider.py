from brockassemble.command import summon_rider


def test_basic_usage():
    result = summon_rider('@s', 'custom:test_mob')
    assert result == '/ride @s summon_rider custom:test_mob'


def test_exclude_slash():
    result = summon_rider('@s', 'custom:test_mob', include_slash=False)
    assert result == 'ride @s summon_rider custom:test_mob'


def test_spawn_event():
    result = summon_rider('@s', 'custom:test_mob', 'custom_spawn')
    assert result == '/ride @s summon_rider custom:test_mob custom_spawn'


def test_name():
    result = summon_rider('@s', 'custom:test_mob', 'custom_spawn', 'testy')
    assert result == (
        '/ride @s summon_rider custom:test_mob custom_spawn "testy"'
    )
