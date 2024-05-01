from brockassemble.component import Component


def test_get_id():
    comp_type = 'component_type'
    comp = Component(comp_type)
    assert comp.get_id() == f'minecraft:{comp_type}'


def test_priority_arg():
    comp_type = 'component_type'
    priority = 0
    comp = Component(comp_type, priority)
    assert comp.json_obj['priority'] == priority
