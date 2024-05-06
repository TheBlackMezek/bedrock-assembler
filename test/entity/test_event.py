from brockassemble.entity import Event, EventRandomizer


_test_id = 'test_event'


def test_get_id_without_namespace():
    event = Event(_test_id)
    assert event.get_id() == _test_id


def test_get_id_with_namespace():
    namespace = 'dev'
    event = Event(_test_id, namespace=namespace)
    assert event.get_id() == f'{namespace}:{_test_id}'


def test_json_add_groups():
    test_value = ['component_group_id']
    event = Event(_test_id, add_groups=test_value)
    assert event.get_json()['add']['component_groups'] == test_value


def test_json_remove_groups():
    test_value = ['component_group_id']
    event = Event(_test_id, remove_groups=test_value)
    assert event.get_json()['remove']['component_groups'] == test_value


def test_json_set_properties():
    prop_id = 'prop_id'
    prop_value = 5
    test_value = {f'property:{prop_id}': prop_value}
    event = Event(_test_id, set_properties=[[prop_id, prop_value]])
    assert event.get_json()['set_property'] == test_value


def test_json_sequential_event():
    test_value_1 = 'tag_1'
    test_value_2 = 'tag_2'
    # add_groups is used here arbitrarily as a way to verify event identity
    seq_event = Event('seq', add_groups=[test_value_1])
    event = Event(
        _test_id,
        add_groups=[test_value_2],
        sequential_events=[seq_event]
    )
    sequence = event.get_json()['sequence']
    assert sequence[0]['add']['component_groups'] == [test_value_2]
    assert sequence[1]['add']['component_groups'] == [test_value_1]


def test_json_next_event():
    test_value = 'next_event'
    event = Event(_test_id, next_event=test_value)
    assert event.get_json()['trigger']['event'] == test_value


def test_json_rnd_add_groups():
    rnd = EventRandomizer()
    test_value = ['component_group_id']
    event = Event(_test_id, add_groups=test_value, randomizers=[rnd])
    sequence = event.get_json()['sequence']
    assert sequence[0]['add']['component_groups'] == test_value


def test_json_rnd_remove_groups():
    rnd = EventRandomizer()
    test_value = ['component_group_id']
    event = Event(_test_id, remove_groups=test_value, randomizers=[rnd])
    sequence = event.get_json()['sequence']
    assert sequence[0]['remove']['component_groups'] == test_value


def test_json_rnd_set_properties():
    rnd = EventRandomizer()
    prop_id = 'prop_id'
    prop_value = 5
    test_value = {f'property:{prop_id}': prop_value}
    event = Event(
        _test_id,
        set_properties=[[prop_id,
        prop_value]],
        randomizers=[rnd]
    )
    sequence = event.get_json()['sequence']
    assert sequence[0]['set_property'] == test_value


def test_json_randomizers():
    test_value = 9001
    rnd = EventRandomizer(weight=test_value)
    event = Event(_test_id, randomizers=[rnd])
    sequence = event.get_json()['sequence']
    assert sequence[0]['randomize'][0]['weight'] == test_value


def test_add_add_group():
    test_value = 'component_group_id'
    event = Event(_test_id)
    event.add_add_group(test_value)
    assert test_value in event._add_groups


def test_add_add_groups():
    test_value1 = 'component_group_id'
    test_value2 = 'component_group_id_2'
    event = Event(_test_id)
    event.add_add_groups([test_value1, test_value2])
    assert test_value1 in event._add_groups
    assert test_value2 in event._add_groups


def test_add_remove_group():
    test_value = 'component_group_id'
    event = Event(_test_id)
    event.add_remove_group(test_value)
    assert test_value in event._remove_groups


def test_add_remove_groups():
    test_value1 = 'component_group_id'
    test_value2 = 'component_group_id_2'
    event = Event(_test_id)
    event.add_remove_groups([test_value1, test_value2])
    assert test_value1 in event._remove_groups
    assert test_value2 in event._remove_groups


def test_add_randomizer():
    rnd = EventRandomizer()
    event = Event(_test_id)
    event.add_randomizer(rnd)
    assert rnd in event._randomizers


def test_add_randomizers():
    rnd1 = EventRandomizer()
    rnd2 = EventRandomizer()
    event = Event(_test_id)
    event.add_randomizers([rnd1, rnd2])
    assert rnd1 in event._randomizers
    assert rnd2 in event._randomizers


def test_add_sequential_event():
    test_event = Event('seq1')
    event = Event(_test_id)
    event.add_sequential_event(test_event)
    assert test_event in event._sequential_events


def test_add_sequential_events():
    test_event1 = Event('seq1')
    test_event2 = Event('seq2')
    event = Event(_test_id)
    event.add_sequential_events([test_event1, test_event2])
    assert test_event1 in event._sequential_events
    assert test_event2 in event._sequential_events


def test_add_set_property_no_quotes():
    prop_id = 'prop_id'
    value = 'prop_value'
    event = Event(_test_id)
    event.add_set_property(prop_id, value, True)
    assert event._set_properties['property:prop_id'] == "prop_value"


def test_add_set_property_with_quotes():
    prop_id = 'prop_id'
    value = 'prop_value'
    event = Event(_test_id)
    event.add_set_property(prop_id, value, False)
    assert event._set_properties['property:prop_id'] == "'prop_value'"
