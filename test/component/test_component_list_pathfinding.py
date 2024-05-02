from brockassemble.component import component_list_pathfinding


_default_target = 'player',
_default_event = 'next_state'


def test_for_targeting_comp():
    comps = component_list_pathfinding(_default_target, _default_event)
    comp_exists = False
    for comp in comps:
        if comp.comp_type == 'behavior.nearest_attackable_target':
            comp_exists = True
            break
    assert comp_exists


def test_for_damage_comp():
    comps = component_list_pathfinding(_default_target, _default_event)
    comp_exists = False
    for comp in comps:
        if comp.comp_type == 'attack':
            comp_exists = True
            break
    assert comp_exists


def test_for_approach_comp():
    comps = component_list_pathfinding(_default_target, _default_event)
    comp_exists = False
    for comp in comps:
        if comp.comp_type == 'behavior.melee_attack':
            comp_exists = True
            break
    assert comp_exists


def test_for_sensor_comp():
    comps = component_list_pathfinding(_default_target, _default_event)
    comp_exists = False
    for comp in comps:
        if comp.comp_type == 'entity_sensor':
            comp_exists = True
            break
    assert comp_exists


def test_targeting_target_family():
    comps = component_list_pathfinding(_default_target, _default_event)
    for comp in comps:
        if comp.comp_type == 'behavior.nearest_attackable_target':
            comp_target = comp.json_obj['entity_types'][0]['filters']['value']
            assert comp_target == _default_target
            break


def test_sensor_target_family():
    comps = component_list_pathfinding(_default_target, _default_event)
    for comp in comps:
        if comp.comp_type == 'entity_sensor':
            comp_target = comp.json_obj['event_filters'][0]['value']
            assert comp_target == _default_target
            break


def test_sensor_range():
    test_value = 1
    comps = component_list_pathfinding(
        _default_target,
        _default_event,
        test_value
    )
    for comp in comps:
        if comp.comp_type == 'entity_sensor':
            assert comp.json_obj['sensor_range'] == test_value
            break


def test_reached_event():
    comps = component_list_pathfinding(_default_target, _default_event)
    for comp in comps:
        if comp.comp_type == 'entity_sensor':
            assert comp.json_obj['event'] == _default_event
            break
