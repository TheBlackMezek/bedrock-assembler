from brockassemble.component import component_variant


def test_basic_usage():
    skin_id = 0
    comp = component_variant(skin_id)
    assert comp.json_obj['value'] == skin_id


def test_component_type():
    comp = component_variant(0)
    assert comp.comp_type == 'variant'
