from brockassemble.command import summon


def test_basic_usage():
    result = summon('custom:test_mob')
    assert result == '/summon custom:test_mob'


def test_exclude_slash():
    result = summon('custom:test_mob', include_slash=False)
    assert result == 'summon custom:test_mob'


def test_position_numbers():
    result = summon('custom:test_mob', x=1, y=2, z=3)
    assert result == '/summon custom:test_mob 1 2 3'


def test_position_strings():
    result = summon('custom:test_mob', x='~1', y='~2', z='~3')
    assert result == '/summon custom:test_mob ~1 ~2 ~3'


def test_rotation():
    result = summon(
        'custom:test_mob',
        x=1,
        y=2,
        z=3,
        y_rot=30,
        x_rot=20
    )
    assert result == '/summon custom:test_mob 1 2 3 30 20'


def test_facing_target():
    result = summon(
        'custom:test_mob',
        x=1,
        y=2,
        z=3,
        facing_target='@s'
    )
    assert result == '/summon custom:test_mob 1 2 3 facing @s'


def test_facing_position_numbers():
    result = summon(
        'custom:test_mob',
        x=1,
        y=2,
        z=3,
        facing_x=10,
        facing_y=20,
        facing_z=30
    )
    assert result == '/summon custom:test_mob 1 2 3 facing 10 20 30'


def test_facing_position_strings():
    result = summon(
        'custom:test_mob',
        x=1,
        y=2,
        z=3,
        facing_x='~10',
        facing_y='~20',
        facing_z='~30'
    )
    assert result == '/summon custom:test_mob 1 2 3 facing ~10 ~20 ~30'


def test_spawn_event():
    result = summon(
        'custom:test_mob',
        x=1,
        y=2,
        z=3,
        facing_target='@s',
        spawn_event='custom_spawn'
    )
    assert result == '/summon custom:test_mob 1 2 3 facing @s custom_spawn'


def test_name_no_facing():
    result = summon(
        'custom:test_mob',
        name='testy'
    )
    assert result == '/summon custom:test_mob "testy"'


def test_name_with_rotation():
    result = summon(
        'custom:test_mob',
        x=1,
        y=2,
        z=3,
        y_rot=30,
        x_rot=20,
        spawn_event='custom_spawn',
        name='testy'
    )
    assert result == '/summon custom:test_mob 1 2 3 30 20 custom_spawn "testy"'


def test_name_with_facing_target():
    result = summon(
        'custom:test_mob',
        x=1,
        y=2,
        z=3,
        facing_target='@s',
        spawn_event='custom_spawn',
        name='testy'
    )
    assert result == (
        '/summon custom:test_mob 1 2 3 facing @s custom_spawn "testy"'
    )


def test_name_with_facing_position():
    result = summon(
        'custom:test_mob',
        x=1,
        y=2,
        z=3,
        facing_x=5,
        facing_y=6,
        facing_z=7,
        spawn_event='custom_spawn',
        name='testy'
    )
    assert result == (
        '/summon custom:test_mob 1 2 3 facing 5 6 7 custom_spawn "testy"'
    )
