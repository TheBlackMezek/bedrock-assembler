from brockassemble.entity import AnimationController, AncoState


_test_id = 'controller.animation.test_anco'
_test_state_id_1 = 'test_state_1'
_test_state_id_2 = 'test_state_2'


def test_add_state():
    anco = AnimationController(_test_id)
    state = AncoState(_test_state_id_1)
    anco.add_state(state)
    assert state in anco._states


def test_add_states():
    anco = AnimationController(_test_id)
    state_1 = AncoState(_test_state_id_1)
    state_2 = AncoState(_test_state_id_2)
    states = [state_1, state_2]
    anco.add_states(states)
    assert state_1 in anco._states
    assert state_2 in anco._states


def test_has_state_true():
    anco = AnimationController(_test_id)
    state = AncoState(_test_state_id_1)
    anco.add_state(state)
    assert anco.has_state(_test_state_id_1)


def test_has_state_false():
    anco = AnimationController(_test_id)
    assert not anco.has_state(_test_state_id_1)


def test_get_state_true():
    anco = AnimationController(_test_id)
    state = AncoState(_test_state_id_1)
    anco.add_state(state)
    assert anco.get_state(_test_state_id_1) is state


def test_get_state_false():
    anco = AnimationController(_test_id)
    assert anco.get_state(_test_state_id_1) is None


def test_json_has_format_version():
    anco = AnimationController(_test_id)
    assert 'format_version' in anco.get_json()


def test_json_has_animation_controllers():
    anco = AnimationController(_test_id)
    assert 'animation_controllers' in anco.get_json()


def test_json_has_anco():
    anco = AnimationController(_test_id)
    assert _test_id in anco.get_json()['animation_controllers']


def test_json_initial_state():
    test_value = 'test_state'
    anco = AnimationController(_test_id, initial_state=test_value)
    anco_json = anco.get_json()['animation_controllers'][_test_id]
    assert anco_json['initial_state'] == test_value


def test_json_states():
    test_value = 'test_state'
    anco = AnimationController(_test_id)
    anco.add_state(AncoState(test_value))
    anco_json = anco.get_json()['animation_controllers'][_test_id]
    assert test_value in anco_json['states']
