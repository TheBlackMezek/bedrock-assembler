from brockassemble.command import tag
from brockassemble.exceptions import MissingParameterError


def test_mode_add():
    result = tag('@s', 'tag1', True)
    assert result == '/tag @s add tag1'


def test_mode_remove():
    result = tag('@s', 'tag1', mode_remove=True)
    assert result == '/tag @s remove tag1'


def test_mode_list():
    result = tag('@s', mode_list=True)
    assert result == '/tag @s list'


def test_exclude_slash():
    result = tag('@s', mode_list=True, include_slash=False)
    assert result == 'tag @s list'


def test_tag_id_missing_error():
    try:
        tag('@s', mode_add=True)
    except MissingParameterError as e:
        assert str(e) == (
            "'tag_id' must be supplied if using 'mode_add' or 'mode_remove'."
        )
    else:
        assert False, (
            "Expected MissingParameterError but no exception was raised."
        )


def test_no_mode_set_error():
    try:
        tag('@s')
    except MissingParameterError as e:
        assert str(e) == (
            "One of the following must be True: "
            "'mode_add', 'mode_remove', or 'mode_list'."
        )
    else:
        assert False, (
            "Expected MissingParameterError but no exception was raised."
        )
