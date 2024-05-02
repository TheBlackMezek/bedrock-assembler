from brockassemble.component import component_no_dmg


def test_deals_no_dmg():
    comp = component_no_dmg()
    assert comp.json_obj['triggers']['deals_damage'] == False


def test_component_type():
    comp = component_no_dmg()
    assert comp.comp_type == 'damage_sensor'
