from brockassemble.entity import EntityProperty


_test_id = 'test_property'
_test_default = 0


def test_json_type():
    test_value = 'test_type'
    prop = EntityProperty(_test_id, _test_default)
    prop._data_type = test_value
    assert prop.get_json()['type'] == test_value


def test_json_default():
    prop = EntityProperty(_test_id, _test_default)
    assert prop.get_json()['default'] == _test_default


def test_json_client_sync():
    test_value = True
    prop = EntityProperty(_test_id, _test_default, client_sync=test_value)
    assert prop.get_json()['client_sync'] == test_value


def test_json_values():
    test_values = [0.0, 1.0]
    prop = EntityProperty(_test_id, _test_default)
    prop._values = test_values
    assert prop.get_json()['values'] == test_values
