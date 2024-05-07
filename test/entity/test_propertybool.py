from brockassemble.entity import PropertyBool


def test_values():
    prop = PropertyBool(
        'test_property',
        False
    )
    assert prop.get_json()['values'] == [False, True]
