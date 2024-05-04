from brockassemble.entity import Animation, AnimTimelineItem


_test_id = 'test_animation'


def test_looping():
    test_value = True
    anim = Animation(_test_id, looping=test_value)
    assert anim.get_json()['loop'] == test_value


def test_anim_len():
    test_value = 2.0
    anim = Animation(_test_id, length=test_value)
    assert anim.get_json()['animation_length'] == test_value


def test_timeline_time():
    test_time_num = 1.0
    test_time_str = '1.0'
    ati = AnimTimelineItem(test_time_num)
    anim = Animation(_test_id, timeline_items=[ati])
    assert test_time_str in anim.get_json()['timeline'].keys()


def test_add_timeline_item():
    test_time_num = 1.0
    test_time_str = '1.0'
    ati = AnimTimelineItem(test_time_num)
    anim = Animation(_test_id)
    anim.add_timeline_item(ati)
    assert test_time_str in anim.get_json()['timeline'].keys()


def test_add_timeline_items():
    ati1 = AnimTimelineItem(1.0)
    ati2 = AnimTimelineItem(2.0)
    anim = Animation(_test_id)
    anim.add_timeline_items([ati1, ati2])
    assert '1.0' in anim.get_json()['timeline'].keys()
    assert '2.0' in anim.get_json()['timeline'].keys()
