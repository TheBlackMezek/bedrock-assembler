from brockassemble.component import component_attack
from brockassemble.exceptions import MissingParameterError


def test_int_dmg():
    dmg = 5
    comp = component_attack(dmg)
    assert comp.json_obj['damage'] == dmg


def test_list_dmg():
    dmg = [3, 5]
    comp = component_attack(dmg)
    assert comp.json_obj['damage'] == dmg


def test_effect_id():
    effect_id = 'slowness'
    comp = component_attack(5, effect_id, 1.0)
    assert comp.json_obj['effect_name'] == effect_id


def test_effect_duration():
    effect_dur = 1.0
    comp = component_attack(5, 'slowness', effect_dur)
    assert comp.json_obj['effect_duration'] == effect_dur


def test_only_effect_id():
    try:
        component_attack(5, 'slowness')
    except MissingParameterError as e:
        assert str(e) == (
            "Either 'effect_id' and 'effect_duration' must both be used, "
            "OR they must both be None"
        )
    else:
        assert False, (
            "Expected MissingParameterError but no exception was raised."
        )


def test_only_effect_dur():
    try:
        component_attack(5, effect_duration=1.0)
    except MissingParameterError as e:
        assert str(e) == (
            "Either 'effect_id' and 'effect_duration' must both be used, "
            "OR they must both be None"
        )
    else:
        assert False, (
            "Expected MissingParameterError but no exception was raised."
        )


def test_component_type():
    comp = component_attack(5)
    assert comp.comp_type == 'attack'
