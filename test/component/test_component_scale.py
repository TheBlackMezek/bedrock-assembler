from brockassemble.component import component_scale


def test_basic_usage():
    skin_id = 0
    comp = component_scale(skin_id)
    assert comp.json_obj['value'] == skin_id


def test_component_type():
    comp = component_scale(0.0)
    assert comp.comp_type == 'scale'
