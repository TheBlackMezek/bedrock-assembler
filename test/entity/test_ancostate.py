from brockassemble.entity import AncoState


_test_id = 'test_state'


def test_json_transitions():
    trans_list = [['state_id', 'query_condition']]
    trans_json = [{'state_id': 'query_condition'}]
    state = AncoState(_test_id, transitions=trans_list)
    assert state.get_json()['transitions'] == trans_json


def test_json_entry_cmds():
    test_value = ['/say Hi']
    state = AncoState(_test_id, entry_commands=test_value)
    assert state.get_json()['on_entry'] == test_value


def test_json_exit_cmds():
    test_value = ['/say Hi']
    state = AncoState(_test_id, exit_commands=test_value)
    assert state.get_json()['on_exit'] == test_value


def test_json_anims():
    test_value = ['test_anim']
    state = AncoState(_test_id, animations=test_value)
    assert state.get_json()['animations'] == test_value


def test_json_transition_time():
    test_value = 1.0
    state = AncoState(_test_id, transition_time=test_value)
    assert state.get_json()['blend_transition'] == test_value


def test_add_entry_cmd():
    test_value = '/say Hi'
    state = AncoState(_test_id)
    state.add_entry_command(test_value)
    assert state.get_json()['on_entry'] == [test_value]


def test_add_entry_cmds():
    test_value = ['/say Hi', '/say Bye']
    state = AncoState(_test_id)
    state.add_entry_commands(test_value)
    assert state.get_json()['on_entry'] == test_value


def test_add_exit_cmd():
    test_value = '/say Hi'
    state = AncoState(_test_id)
    state.add_exit_command(test_value)
    assert state.get_json()['on_exit'] == [test_value]


def test_add_exit_cmds():
    test_value = ['/say Hi', '/say Bye']
    state = AncoState(_test_id)
    state.add_exit_commands(test_value)
    assert state.get_json()['on_exit'] == test_value


def test_add_animation():
    test_value = 'test_anim'
    state = AncoState(_test_id)
    state.add_animation(test_value)
    assert state.get_json()['animations'] == [test_value]


def test_add_animations():
    test_value = ['test_anim_1', 'test_anim_2']
    state = AncoState(_test_id)
    state.add_animations(test_value)
    assert state.get_json()['animations'] == test_value


def test_add_transition():
    test_state = 'test_state'
    test_condition = 'query.test_condition'
    state = AncoState(_test_id)
    state.add_transition(test_state, test_condition)
    assert state.get_json()['transitions'] == [{test_state: test_condition}]


def test_add_transitions():
    trans_list = [['state_id', 'query_condition'], ['state_2', 'cond_2']]
    trans_json = [{'state_id': 'query_condition'}, {'state_2': 'cond_2'}]
    state = AncoState(_test_id)
    state.add_transitions(trans_list)
    assert state.get_json()['transitions'] == trans_json
