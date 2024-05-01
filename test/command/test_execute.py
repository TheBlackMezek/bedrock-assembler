from brockassemble.command import execute


def test_no_optional_parameters():
    cmd = 'say TEST'
    assert execute(cmd) == '/execute ~ ~ ~ say TEST'


def test_with_selector():
    cmd = 'say TEST'
    selector = '@p'
    assert execute(cmd, selector) == '/execute @p ~ ~ ~ say TEST'


def test_with_number_positions():
    cmd = 'say TEST'
    assert execute(cmd, x=1, y=2, z=3) == '/execute 1 2 3 say TEST'


def test_with_string_positions():
    cmd = 'say TEST'
    assert execute(cmd, x='~1', y='~2', z='~3') == '/execute ~1 ~2 ~3 say TEST'


def test_exclude_slash():
    cmd = 'say TEST'
    assert execute(cmd, include_slash=False) == 'execute ~ ~ ~ say TEST'


def test_detect_block_no_optional_parameters():
    cmd = 'say TEST'
    result = execute(cmd, detect_block='stone')
    assert result == '/execute ~ ~ ~ detect ~ ~ ~ stone 0 say TEST'


def test_detect_block_data_id():
    cmd = 'say TEST'
    result = execute(cmd, detect_block='stone', detect_data_id=3)
    assert result == '/execute ~ ~ ~ detect ~ ~ ~ stone 3 say TEST'


def test_detect_block_number_positions():
    cmd = 'say TEST'
    result = execute(
        cmd,
        detect_block='stone',
        detect_x=3,
        detect_y=4,
        detect_z=5
    )
    assert result == '/execute ~ ~ ~ detect 3 4 5 stone 0 say TEST'


def test_detect_block_string_positions():
    cmd = 'say TEST'
    result = execute(
        cmd,
        detect_block='stone',
        detect_x='~3',
        detect_y='~4',
        detect_z='~5'
    )
    assert result == '/execute ~ ~ ~ detect ~3 ~4 ~5 stone 0 say TEST'
