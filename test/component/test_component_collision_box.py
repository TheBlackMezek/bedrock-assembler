from brockassemble.component import component_collision_box


def test_arg_range():
    test_value = 1.0
    comp = component_collision_box(test_value, 2.0)
    assert comp.json_obj['width'] == test_value


def test_arg_dmg():
    test_value = 2.0
    comp = component_collision_box(1.0, test_value)
    assert comp.json_obj['height'] == test_value


def test_component_type():
    comp = component_collision_box(1.0, 2.0)
    assert comp.comp_type == 'collision_box'
