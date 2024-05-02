from brockassemble.component import tag_sensor


_test_tag = 'test_tag'
_test_event = 'test_event'


def test_tag():
    comp = tag_sensor(_test_tag, _test_event)
    trigger = comp.json_obj['triggers'][0]
    assert trigger['filters']['value'] == _test_tag


def test_event():
    comp = tag_sensor(_test_tag, _test_event)
    trigger = comp.json_obj['triggers'][0]
    assert trigger['event'] == _test_event


def test_component_type():
    comp = tag_sensor(_test_tag, _test_event)
    assert comp.comp_type == 'environment_sensor'
