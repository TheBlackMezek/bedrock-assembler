from brockassemble.component import component_follow_range


def test_prop_max():
    test_value = 60.0
    comp = component_follow_range(test_value)
    assert comp.json_obj['max'] == test_value


def test_prop_value():
    test_value = 60.0
    comp = component_follow_range(test_value)
    assert comp.json_obj['value'] == test_value


def test_component_type():
    comp = component_follow_range(60.0)
    assert comp.comp_type == 'follow_range'
