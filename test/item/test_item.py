from brockassemble.item import Item


_test_namespace = 'testspace'
_test_name = 'Test Item'
_test_id = 'test_id'
_test_tex_name = 'test_texture'
_test_category = 'Tools'


def test_init_namespace():
    item = Item(_test_namespace, _test_name)
    assert item.namespace == _test_namespace
