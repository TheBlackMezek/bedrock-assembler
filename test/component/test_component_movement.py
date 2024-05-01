from brockassemble.component import component_movement


def test_basic_usage():
    speed = 0.0
    comp = component_movement(speed)
    assert comp.json_obj['value'] == speed


def test_component_type():
    comp = component_movement(0.0)
    assert comp.comp_type == 'movement'
