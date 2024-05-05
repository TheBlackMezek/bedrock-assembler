from brockassemble.entity import EventRandomizer


def test_weight():
    test_value = 10
    er = EventRandomizer(test_value)
    assert er.get_json()['weight'] == test_value


def test_add_groups():
    test_value = ['component_group_id']
    er = EventRandomizer(add_groups=test_value)
    assert er.get_json()['add']['component_groups'] == test_value


def test_remove_groups():
    test_value = ['component_group_id']
    er = EventRandomizer(remove_groups=test_value)
    assert er.get_json()['remove']['component_groups'] == test_value


def test_set_properties():
    test_value = {'property_id': 'new_value'}
    er = EventRandomizer(set_properties=test_value)
    assert er.get_json()['set_property'] == test_value
