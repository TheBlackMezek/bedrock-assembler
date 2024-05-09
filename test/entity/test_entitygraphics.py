from brockassemble.entity import EntityGraphics


_test_id = 'test_entity'
_test_namespace = 'dev'


def test_get_id():
    graphics = EntityGraphics(_test_namespace, _test_id)
    assert graphics.get_id() == f'{_test_namespace}:{_test_id}'


def test_tex_path_from_id():
    graphics = EntityGraphics(_test_namespace, _test_id)
    assert graphics.texture_path == 'textures/entity/'+_test_id


def test_tex_path_from_str():
    test_value = 'test_texture'
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        texture_path=test_value
    )
    assert graphics.texture_path == 'textures/entity/'+test_value


def test_tex_path_from_dict():
    test_value = 'test_texture'
    tex_rsc_id = 'local_tex_id'
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        texture_path={tex_rsc_id: test_value}
    )
    assert graphics.texture_path[tex_rsc_id] == 'textures/entity/'+test_value


def test_geo_id_from_id():
    graphics = EntityGraphics(_test_namespace, _test_id)
    assert graphics.geo == 'geometry.'+_test_id


def test_geo_id_from_str():
    test_value = 'test_geo'
    graphics = EntityGraphics(_test_namespace, _test_id, geo=test_value)
    assert graphics.geo == 'geometry.'+test_value


def test_geo_id_from_dict():
    test_value = 'test_geo'
    geo_rsc_id = 'local_geo_id'
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        geo={geo_rsc_id: test_value}
    )
    assert graphics.geo[geo_rsc_id] == 'geometry.'+test_value
