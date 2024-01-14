from brockassemble.command import effect
from brockassemble.exceptions import MissingParameterError


def test_basic_usage():
    result = effect('@s', 'poison')
    assert result == '/effect @s poison 1 1'


def test_no_clear_or_effect_error():
    try:
        effect('@s')
    except MissingParameterError as e:
        assert str(e) == (
            "Either 'effect' must be provided OR 'clear' must be True."
        )
    else:
        assert False, (
            "Expected MissingParameterError but no exception was raised."
        )


def test_clear():
    result = effect('@s', clear=True)
    assert result == '/effect @s clear'


def test_exclude_slash():
    result = effect('@s', 'poison', include_slash=False)
    assert result == 'effect @s poison 1 1'


def test_duration():
    result = effect('@s', 'poison', duration=5)
    assert result == '/effect @s poison 5 1'


def test_level():
    result = effect('@s', 'poison', level=5)
    assert result == '/effect @s poison 1 5'


def test_hide_particles():
    result = effect('@s', 'poison', hide_particles=True)
    assert result == '/effect @s poison 1 1 true'
