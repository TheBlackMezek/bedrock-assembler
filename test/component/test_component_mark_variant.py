from brockassemble.component import component_mark_variant


def test_basic_usage():
    mark_variant = 0
    comp = component_mark_variant(mark_variant)
    assert comp.json_obj['value'] == mark_variant


def test_component_type():
    comp = component_mark_variant(0)
    assert comp.comp_type == 'mark_variant'
