from brockassemble.entity import PropertyEnum


def test_int_values():
    test_values = [1, 3, 5]
    prop = PropertyEnum(
        'test_property',
        test_values,
        1
    )
    assert prop.get_json()['values'] == test_values


def test_str_values():
    test_values = ['hi', 'bye', 'yes']
    prop = PropertyEnum(
        'test_property',
        test_values,
        'hi'
    )
    assert prop.get_json()['values'] == test_values
