from brockassemble.item import Item


_test_namespace = 'testspace'
_test_name = 'Test Item'
_test_id_from_name = 'test_item'
_test_id = 'test_id'
_test_tex_name = 'test_texture'
_test_category = 'Tools'


def test_init_namespace():
    item = Item(_test_namespace, _test_name)
    assert item.namespace == _test_namespace


def test_init_name():
    item = Item(_test_namespace, _test_name)
    assert item._name == _test_name


def test_init_items():
    item = Item(_test_namespace, _test_name, category=_test_category)
    assert item.category == _test_category


def test_init_id_with_arg():
    item = Item(_test_namespace, _test_name, id=_test_id)
    assert item.identifier == _test_id


def test_init_id_from_name():
    item = Item(_test_namespace, _test_name)
    assert item.identifier == _test_id_from_name


def test_init_tex_with_arg():
    item = Item(_test_namespace, _test_name, texture_name=_test_tex_name)
    assert item.texture_name == _test_tex_name


def test_init_tex_from_id():
    item = Item(_test_namespace, _test_name)
    assert item.texture_name == _test_id_from_name


def test_set_tex_name_variable():
    test_value = 'new_texture'
    item = Item(_test_namespace, _test_name)
    item.texture_name = test_value
    assert item.texture_name == test_value


def test_set_tex_name_component():
    test_value = 'new_texture'
    item = Item(_test_namespace, _test_name)
    item.texture_name = test_value
    assert item._icon_comp.json_obj['texture'] == test_value
