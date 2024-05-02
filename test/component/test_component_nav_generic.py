from brockassemble.component import component_nav_generic


def test_arg_path_water():
    test_value = False
    comp = component_nav_generic(can_path_over_water=test_value)
    assert comp.json_obj['can_path_over_water'] == test_value


def test_arg_avoid_water():
    test_value = False
    comp = component_nav_generic(avoid_water=test_value)
    assert comp.json_obj['avoid_water'] == test_value


def test_arg_pass_doors():
    test_value = False
    comp = component_nav_generic(can_pass_doors=test_value)
    assert comp.json_obj['can_pass_doors'] == test_value


def test_arg_open_doors():
    test_value = False
    comp = component_nav_generic(can_open_doors=test_value)
    assert comp.json_obj['can_open_doors'] == test_value


def test_arg_damage_blocks():
    test_value = False
    comp = component_nav_generic(avoid_damage_blocks=test_value)
    assert comp.json_obj['avoid_damage_blocks'] == test_value


def test_component_type():
    comp = component_nav_generic()
    assert comp.comp_type == 'navigation.generic'
