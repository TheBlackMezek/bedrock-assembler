from brockassemble.component import component_no_knockback


def test_resistance_value():
    test_value = 1.0
    comp = component_no_knockback()
    assert comp.json_obj['value'] == test_value


def test_component_type():
    comp = component_no_knockback()
    assert comp.comp_type == 'knockback_resistance'
