from brockassemble.component import component_stroll


def test_default_priority():
    comp = component_stroll()
    assert comp.json_obj['priority'] == 5


def test_default_speed():
    comp = component_stroll()
    assert comp.json_obj['speed_multiplier'] == 1.0


def test_arg_priority():
    comp = component_stroll(priority=1)
    assert comp.json_obj['priority'] == 1


def test_arg_speed():
    comp = component_stroll(speed=2.0)
    assert comp.json_obj['speed_multiplier'] == 2.0


def test_component_type():
    comp = component_stroll()
    assert comp.comp_type == 'behavior.random_stroll'
