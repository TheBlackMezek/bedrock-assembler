from brockassemble.command import tp
from brockassemble.exceptions import MissingParameterError


def test_basic_usage():
    assert tp(victim_selector='@p', target_selector='@s') == '/tp @p @s'


def test_no_target_error():
    try:
        tp(victim_selector='@p')
    except MissingParameterError as e:
        assert str(e) == (
            "Either 'target_selector' OR 'x', 'y', and 'z' "
            "MUST be provided to tp()"
        )
    else:
        assert False, (
            "Expected MissingParameterError but no exception was raised."
        )


def test_exclude_slash():
    result = tp(
        victim_selector='@p',
        target_selector='@s',
        include_slash=False
    )
    assert result == 'tp @p @s'


def test_number_positions():
    result = tp(victim_selector='@p', x=1, y=2, z=3)
    assert result == '/tp @p 1 2 3'


def test_string_positions():
    result = tp(victim_selector='@p', x='~1', y='~2', z='~3')
    assert result == '/tp @p ~1 ~2 ~3'


def test_rotations():
    result = tp(
        victim_selector='@p',
        target_selector='@s',
        x_rot=90,
        y_rot=-20
    )
    assert result == '/tp @p @s 90 -20'


def test_facing_selector():
    result = tp(
        victim_selector='@p',
        target_selector='@s',
        facing_selector='@s'
    )
    assert result == '/tp @p @s @s'


def test_facing_position_numbers():
    result = tp(
        victim_selector='@p',
        target_selector='@s',
        facing_x=1,
        facing_y=2,
        facing_z=3
    )
    assert result == '/tp @p @s 1 2 3'


def test_facing_position_strings():
    result = tp(
        victim_selector='@p',
        target_selector='@s',
        facing_x='~1',
        facing_y='~2',
        facing_z='~3'
    )
    assert result == '/tp @p @s ~1 ~2 ~3'


def test_check_for_blocks():
    result = tp(
        victim_selector='@p',
        target_selector='@s',
        check_for_blocks=True
    )
    assert result == '/tp @p @s true'


def test_ordering_first_set():
    result = tp(
        victim_selector='@p',
        x=1,
        y=2,
        z=3,
        x_rot=10,
        y_rot=20,
        check_for_blocks=True
    )
    assert result == '/tp @p 1 2 3 10 20 true'


def test_ordering_second_set():
    result = tp(
        victim_selector='@p',
        target_selector='@s',
        facing_selector='@e',
        check_for_blocks=True
    )
    assert result == '/tp @p @s @e true'
