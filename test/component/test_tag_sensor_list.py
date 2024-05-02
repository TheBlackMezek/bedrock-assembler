from brockassemble.component import tag_sensor_list


_test_tags = ['test_tag']
_test_events = ['test_event']


def test_tag():
    comp = tag_sensor_list(_test_tags, _test_events)
    trigger = comp.json_obj['triggers'][0]
    assert trigger['filters']['value'] == _test_tags[0]


def test_event():
    comp = tag_sensor_list(_test_tags, _test_events)
    trigger = comp.json_obj['triggers'][0]
    assert trigger['event'] == _test_events[0]


def test_tag_not_a_str():
    try:
        tag_sensor_list([1], _test_events)
    except TypeError as e:
        assert str(e) == (
            "An element of tags is type <class 'int'> "
            "instead of a string"
        )
    else:
        assert False, ("Expected TypeError but no exception was raised.")


def test_event_not_a_str():
    try:
        tag_sensor_list(_test_tags, [1])
    except TypeError as e:
        assert str(e) == (
            "An element of events is type <class 'int'> "
            "instead of a string"
        )
    else:
        assert False, ("Expected TypeError but no exception was raised.")


def test_component_type():
    comp = tag_sensor_list(_test_tags, _test_events)
    assert comp.comp_type == 'environment_sensor'