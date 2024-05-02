from brockassemble.component import component_shooter


_test_projectile_id = 'minecraft:arrow'


def test_projectile_id():
    comp = component_shooter(_test_projectile_id)
    assert comp.json_obj['def'] == _test_projectile_id


def test_potion_effect():
    test_value = 5
    comp = component_shooter(_test_projectile_id, 5)
    assert comp.json_obj['aux_val'] == test_value


def test_component_type():
    comp = component_shooter(_test_projectile_id)
    assert comp.comp_type == 'shooter'
