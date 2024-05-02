from brockassemble.component import component_rideable


_test_seats_valid = [
    [0.0, 0.5, 1.0]
]

_families_valid = ['mob']


def test_valid_seat_positions():
    comp = component_rideable(_test_seats_valid, _families_valid)
    assert comp.json_obj['seats'][0]['position'] == _test_seats_valid[0]


def test_seat_count():
    comp = component_rideable(_test_seats_valid, _families_valid)
    assert comp.json_obj['seat_count'] == len(_test_seats_valid)


def test_valid_families():
    comp = component_rideable(_test_seats_valid, _families_valid)
    assert comp.json_obj['family_types'] == _families_valid


def test_valid_pull_in_entities():
    test_value = True
    comp = component_rideable(_test_seats_valid, _families_valid, test_value)
    assert comp.json_obj['pull_in_entities'] == test_value


def test_seats_not_a_list():
    try:
        component_rideable('not_a_list', _families_valid)
    except TypeError as e:
        assert str(e) == (
            "seat_positions is type <class 'str'> instead of a list"
        )
    else:
        assert False, ("Expected TypeError but no exception was raised.")


def test_seat_element_not_a_list():
    try:
        component_rideable(['not_a_list'], _families_valid)
    except TypeError as e:
        assert str(e) == (
            "An element of seat_positions is type <class 'str'> "
            "instead of a list"
        )
    else:
        assert False, ("Expected TypeError but no exception was raised.")


def test_seat_element_invalid_len():
    try:
        component_rideable([[0.0]], _families_valid)
    except ValueError as e:
        assert str(e) == (
            "An element of seat_positions has 1 elements "
            "but it must have exactly 3"
        )
    else:
        assert False, ("Expected ValueError but no exception was raised.")


def test_seat_element_nan():
    try:
        component_rideable([['not_a_number', 0.0, 1]], _families_valid)
    except TypeError as e:
        assert str(e) == (
            "An element in a seat position is type <class 'str'> "
            "instead of a number"
        )
    else:
        assert False, ("Expected TypeError but no exception was raised.")


def test_families_not_a_list():
    try:
        component_rideable(_test_seats_valid, 'not_a_list')
    except TypeError as e:
        assert str(e) == (
            "family_types is type <class 'str'> instead of a list"
        )
    else:
        assert False, ("Expected TypeError but no exception was raised.")


def test_family_not_a_str():
    try:
        component_rideable(_test_seats_valid, [1])
    except TypeError as e:
        assert str(e) == (
            "An element of family_types is type <class 'int'> "
            "instead of a string"
        )
    else:
        assert False, ("Expected TypeError but no exception was raised.")


def test_pull_in_entities_type_error():
    try:
        component_rideable(_test_seats_valid, _families_valid, 'not_a_bool')
    except TypeError as e:
        assert str(e) == (
            "pull_in_entities is type <class 'str'> instead of a bool"
        )
    else:
        assert False, ("Expected TypeError but no exception was raised.")


def test_component_type():
    comp = component_rideable(_test_seats_valid, _families_valid)
    assert comp.comp_type == 'rideable'
