from brockassemble.component import component_random_look


def test_default_priority():
    comp = component_random_look()
    assert comp.json_obj['priority'] == 8


def test_component_type():
    comp = component_random_look()
    assert comp.comp_type == 'behavior.random_look_around'
