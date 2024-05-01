from brockassemble.component import component_variant


def test_basic_usage():
    variant = 0
    comp = component_variant(variant)
    assert comp.json_obj['value'] == variant


def test_component_type():
    comp = component_variant(0)
    assert comp.comp_type == 'variant'
