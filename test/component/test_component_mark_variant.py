from brockassemble.component import component_mark_variant


def test_basic_usage():
    skin_id = 0
    comp = component_mark_variant(skin_id)
    assert comp.json_obj['value'] == skin_id


def test_component_type():
    comp = component_mark_variant(0)
    assert comp.comp_type == 'mark_variant'
