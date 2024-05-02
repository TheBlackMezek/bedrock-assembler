from brockassemble.component import component_scale


def test_basic_usage():
    scale = 0.0
    comp = component_scale(scale)
    assert comp.json_obj['value'] == scale


def test_component_type():
    comp = component_scale(0.0)
    assert comp.comp_type == 'scale'
