from brockassemble.entity import ComponentGroup
from brockassemble.component import Component


_test_id = 'test_group'


def test_get_id_without_namespace():
    group = ComponentGroup(_test_id)
    assert group.get_id() == _test_id


def test_get_id_with_namespace():
    namespace = 'dev'
    group = ComponentGroup(_test_id, namespace=namespace)
    assert group.get_id() == f'{namespace}:{_test_id}'


def test_skin_id():
    test_value = 1
    found_value = None
    group = ComponentGroup(_test_id, skin_id=test_value)
    for comp in group._components:
        if comp.comp_type == 'skin_id':
            found_value = comp.json_obj['value']
            break
    assert found_value == test_value


def test_timer_len():
    test_value = 1.0
    found_value = None
    group = ComponentGroup(
        _test_id,
        timer_len=test_value,
        timer_event='test_event'
    )
    for comp in group._components:
        if comp.comp_type == 'timer':
            found_value = comp.json_obj['time']
            break
    assert found_value == test_value


def test_timer_event():
    test_value = 'test_event'
    found_value = None
    group = ComponentGroup(
        _test_id,
        timer_len=1.0,
        timer_event=test_value
    )
    for comp in group._components:
        if comp.comp_type == 'timer':
            found_value = comp.json_obj['time_down_event']['event']
            break
    assert found_value == test_value


def test_hp():
    test_value = 20
    found_value = None
    group = ComponentGroup(
        _test_id,
        hp=test_value
    )
    for comp in group._components:
        if comp.comp_type == 'health':
            found_value = comp.json_obj['value']
            break
    assert found_value == test_value


def test_attack():
    test_value = 20
    found_value = None
    group = ComponentGroup(
        _test_id,
        attack=test_value
    )
    for comp in group._components:
        if comp.comp_type == 'attack':
            found_value = comp.json_obj['damage']
            break
    assert found_value == test_value


def test_move_speed():
    test_value = 2.4
    found_value = None
    group = ComponentGroup(
        _test_id,
        move_speed=test_value
    )
    for comp in group._components:
        if comp.comp_type == 'movement':
            found_value = comp.json_obj['value']
            break
    assert found_value == test_value


def test_has_physics():
    found_comp = False
    group = ComponentGroup(
        _test_id,
        has_physics=True
    )
    for comp in group._components:
        if comp.comp_type == 'physics':
            found_comp = True
            break
    assert found_comp


def test_no_damage():
    found_comp = False
    group = ComponentGroup(
        _test_id,
        no_damage=True
    )
    for comp in group._components:
        if comp.comp_type == 'damage_sensor':
            found_comp = True
            break
    assert found_comp


def test_scale():
    test_value = 2.0
    found_value = None
    group = ComponentGroup(
        _test_id,
        scale=test_value
    )
    for comp in group._components:
        if comp.comp_type == 'scale':
            found_value = comp.json_obj['value']
            break
    assert found_value == test_value


def test_add_component():
    comp_id = 'test_component'
    found_comp = False
    group = ComponentGroup(_test_id)
    group.add_component(Component(comp_id))
    for comp in group._components:
        if comp.comp_type == comp_id:
            found_comp = True
            break
    assert found_comp


def test_add_component_list():
    comp_id1 = 'test_component1'
    comp_id2 = 'test_component2'
    found_comp1 = False
    found_comp2 = False
    group = ComponentGroup(_test_id)
    group.add_component_list([Component(comp_id1), Component(comp_id2)])
    for comp in group._components:
        if comp.comp_type == comp_id1:
            found_comp1 = True
        if comp.comp_type == comp_id2:
            found_comp2 = True
    assert found_comp1
    assert found_comp2


def test_get_json():
    comp_id = 'test_component'
    comp = Component(comp_id)
    group = ComponentGroup(_test_id)
    group.add_component(comp)
    assert comp.get_id() in group.get_json().keys()
