from brockassemble.component import component_melee_attack


def test_arg_speed_mult():
    test_value = 1.0
    comp = component_melee_attack(speed_multiplier=test_value)
    assert comp.json_obj['speed_multiplier'] == test_value


def test_arg_track():
    test_value = True
    comp = component_melee_attack(track_target=test_value)
    assert comp.json_obj['track_target'] == test_value


def test_arg_reach():
    test_value = 1.0
    comp = component_melee_attack(reach_multiplier=test_value)
    assert comp.json_obj['reach_multiplier'] == test_value


def test_component_type():
    comp = component_melee_attack()
    assert comp.comp_type == 'behavior.melee_attack'
