from brockassemble.entity import (
    Behaviors,
    Animation,
    EntityProperty,
    Event,
    ComponentGroup
)
from brockassemble.component import Component


_test_id = 'test_entity'
_test_namespace = 'dev'


def test_get_id():
    bvr = Behaviors(_test_namespace, _test_id)
    assert bvr.get_id() == f'{_test_namespace}:{_test_id}'


def test_add_banco():
    test_value = 'controller.animation.test_banco'
    bvr = Behaviors(_test_namespace, _test_id)
    bvr.add_banco(test_value)
    assert test_value in bvr._bancos


def test_add_animation():
    anim = Animation('test_anim')
    bvr = Behaviors(_test_namespace, _test_id)
    bvr.add_animation(anim)
    assert anim in bvr._animations


def test_get_event_exists():
    event_id = 'test_event'
    event = Event(event_id)
    bvr = Behaviors(_test_namespace, _test_id)
    bvr._events.append(event)
    assert bvr.get_event(event_id) is event


def test_get_event_not_exists():
    event_id = 'test_event'
    bvr = Behaviors(_test_namespace, _test_id)
    assert bvr.get_event(event_id) is None


def test_add_entity_property():
    prop = EntityProperty('test_prop', 0)
    bvr = Behaviors(_test_namespace, _test_id)
    bvr.add_property(prop)
    assert prop in bvr._properties


def test_get_component_exists():
    comp_id = 'test_comp'
    comp = Component(comp_id)
    bvr = Behaviors(_test_namespace, _test_id)
    bvr._components.append(comp)
    assert bvr.get_component(comp_id) is comp


def test_get_component_not_exists():
    comp_id = 'test_comp'
    bvr = Behaviors(_test_namespace, _test_id)
    assert bvr.get_component(comp_id) is None


def test_json_has_minecraft_entity():
    bvr = Behaviors(_test_namespace, _test_id)
    assert 'minecraft:entity' in bvr.get_json()


def test_json_has_format_version():
    bvr = Behaviors(_test_namespace, _test_id)
    assert 'format_version' in bvr.get_json()


def test_json_has_description():
    bvr = Behaviors(_test_namespace, _test_id)
    entity = bvr.get_json()['minecraft:entity']
    assert 'description' in entity


def test_json_identifier():
    bvr = Behaviors(_test_namespace, _test_id)
    desc = bvr.get_json()['minecraft:entity']['description']
    assert desc['identifier'] == f'{_test_namespace}:{_test_id}'


def test_json_spawnable():
    test_value = True
    bvr = Behaviors(_test_namespace, _test_id)
    bvr.is_spawnable = test_value
    desc = bvr.get_json()['minecraft:entity']['description']
    assert desc['is_spawnable'] == test_value


def test_json_summonable():
    test_value = True
    bvr = Behaviors(_test_namespace, _test_id)
    bvr.is_summonable = test_value
    desc = bvr.get_json()['minecraft:entity']['description']
    assert desc['is_summonable'] == test_value


def test_json_experimental():
    test_value = True
    bvr = Behaviors(_test_namespace, _test_id)
    bvr.is_experimental = test_value
    desc = bvr.get_json()['minecraft:entity']['description']
    assert desc['is_experimental'] == test_value


def test_json_banco_anim_dict():
    banco_id = 'controller.animation.test_banco'
    bvr = Behaviors(_test_namespace, _test_id)
    bvr.add_banco(banco_id)
    desc = bvr.get_json()['minecraft:entity']['description']
    assert desc['animations']['banco_0'] == banco_id


def test_json_banco_animate_list():
    bvr = Behaviors(_test_namespace, _test_id)
    bvr.add_banco('controller.animation.test_banco')
    desc = bvr.get_json()['minecraft:entity']['description']
    assert {'banco_0': '1'} in desc['scripts']['animate']


def test_json_animations():
    banim_id = 'animation.test_anim'
    bvr = Behaviors(_test_namespace, _test_id)
    bvr.add_animation(Animation(banim_id))
    desc = bvr.get_json()['minecraft:entity']['description']
    assert banim_id in desc['animations']


def test_json_entity_properties():
    prop_id = 'test_prop'
    prop = EntityProperty(prop_id, 0)
    bvr = Behaviors(_test_namespace, _test_id)
    bvr.add_property(prop)
    desc = bvr.get_json()['minecraft:entity']['description']
    assert f'property:{prop_id}' in desc['properties']


def test_json_components():
    comp_id = 'test_comp'
    bvr = Behaviors(_test_namespace, _test_id)
    bvr._components.append(Component(comp_id))
    entity = bvr.get_json()['minecraft:entity']
    assert f'minecraft:{comp_id}' in entity['components']


def test_json_component_groups():
    group_id = 'test_group'
    bvr = Behaviors(_test_namespace, _test_id)
    bvr._component_groups.append(ComponentGroup(group_id))
    entity = bvr.get_json()['minecraft:entity']
    assert group_id in entity['component_groups']


def test_json_events():
    event_id = 'test_event'
    bvr = Behaviors(_test_namespace, _test_id)
    bvr._events.append(Event(event_id))
    entity = bvr.get_json()['minecraft:entity']
    assert event_id in entity['events']


def test_json_spawn_event():
    bvr = Behaviors(_test_namespace, _test_id)
    bvr._spawn_groups.append('test_group')
    entity = bvr.get_json()['minecraft:entity']
    assert 'minecraft:entity_spawned' in entity['events']


def test_json_spawn_groups():
    test_value = 'test_group'
    bvr = Behaviors(_test_namespace, _test_id)
    bvr._spawn_groups.append(test_value)
    entity = bvr.get_json()['minecraft:entity']
    event = entity['events']['minecraft:entity_spawned']
    assert test_value in event['add']['component_groups']


def test_resolve_lstate_branches():
    state_id = 'state_0'
    branch_name = 'test_group'
    event_id = 'test_event'
    bvr = Behaviors(_test_namespace, _test_id)
    bvr._lstate_names[branch_name] = [state_id]
    bvr._events.append(Event(event_id, add_groups=[branch_name]))
    entity = bvr.get_json()['minecraft:entity']
    event = entity['events'][event_id]
    assert state_id in event['add']['component_groups']
