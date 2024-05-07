from brockassemble.entity import PropertyRange


_test_id = 'test_property'
_test_min = 0
_test_max = 10
_test_default = 5


def test_min():
    prop = PropertyRange(
        _test_id,
        _test_min,
        _test_max,
        _test_default
    )
    assert prop.get_json()['range'][0] == _test_min


def test_max():
    prop = PropertyRange(
        _test_id,
        _test_min,
        _test_max,
        _test_default
    )
    assert prop.get_json()['range'][1] == _test_max
