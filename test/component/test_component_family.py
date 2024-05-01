from brockassemble.component import component_family


def test_basic_usage():
    families = ['mob', 'animal']
    comp = component_family(families)
    assert comp.json_obj['family'] == families


def test_component_type():
    comp = component_family(['mob'])
    assert comp.comp_type == 'type_family'
