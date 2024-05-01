from brockassemble.component import component_health


def test_prop_max():
    test_value = 20
    comp = component_health(test_value)
    assert comp.json_obj['max'] == test_value


def test_prop_value():
    test_value = 20
    comp = component_health(test_value)
    assert comp.json_obj['value'] == test_value


def test_component_type():
    comp = component_health(20)
    assert comp.comp_type == 'health'
