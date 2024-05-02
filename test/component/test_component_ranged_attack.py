from brockassemble.component import component_ranged_attack


def test_arg_range():
    test_value = 1.0
    comp = component_ranged_attack(attack_range=test_value)
    assert comp.json_obj['attack_radius'] == test_value


def test_arg_interval_min():
    test_value = True
    comp = component_ranged_attack(interval_min=test_value)
    assert comp.json_obj['attack_interval_min'] == test_value


def test_arg_reach():
    test_value = 1.0
    comp = component_ranged_attack(interval_max=test_value)
    assert comp.json_obj['attack_interval_max'] == test_value


def test_component_type():
    comp = component_ranged_attack()
    assert comp.comp_type == 'behavior.ranged_attack'
