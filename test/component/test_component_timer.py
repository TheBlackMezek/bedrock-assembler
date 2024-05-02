from brockassemble.component import component_timer


def test_event():
    event = 'event_name'
    comp = component_timer(1.0, event)
    assert comp.json_obj['time_down_event']['event'] == event


def test_length():
    length = 1.0
    comp = component_timer(length, 'event_name')
    assert comp.json_obj['time'] == length


def test_random_interval():
    comp = component_timer(1.0, 'event_name')
    assert comp.json_obj['randomInterval'] == False


def test_component_type():
    comp = component_timer(1.0, 'event_name')
    assert comp.comp_type == 'timer'
