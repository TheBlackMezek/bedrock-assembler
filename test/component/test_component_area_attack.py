from brockassemble.component import component_area_attack


def test_arg_range():
    test_value = 1.0
    comp = component_area_attack(test_value, 5)
    assert comp.json_obj['damage_range'] == test_value


def test_arg_dmg():
    test_value = 5
    comp = component_area_attack(1.0, test_value)
    assert comp.json_obj['damage_per_tick'] == test_value


def test_component_type():
    comp = component_area_attack(1.0, 5)
    assert comp.comp_type == 'area_attack'
