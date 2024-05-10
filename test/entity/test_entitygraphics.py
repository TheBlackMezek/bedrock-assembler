from brockassemble.entity import EntityGraphics, AnimationController


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


def test_add_animations_none_existing():
    test_key = 'walk'
    test_value = 'animation.test_entity.walk'
    test_dict = {test_key: test_value}
    graphics = EntityGraphics(_test_namespace, _test_id)
    graphics.add_animations(test_dict)
    assert graphics._anim_obj == test_dict


def test_add_animations_existing_anims():
    test_key1 = 'walk'
    test_value1 = 'animation.test_entity.walk'
    test_key2 = 'attack'
    test_value2 = 'animation.test_entity.attack'
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        animations={test_key2: test_value2}
    )
    graphics.add_animations({test_key1: test_value1})
    assert graphics._anim_obj[test_key1] == test_value1
    assert graphics._anim_obj[test_key2] == test_value2


def test_add_particles_none_existing():
    test_key = 'sparkle'
    test_value = 'particle.sparkle'
    test_dict = {test_key: test_value}
    graphics = EntityGraphics(_test_namespace, _test_id)
    graphics.add_particles(test_dict)
    assert graphics._particle_obj == test_dict


def test_add_particles_existing_anims():
    test_key1 = 'sparkle'
    test_value1 = 'particle.sparkle'
    test_key2 = 'swirl'
    test_value2 = 'particle.swirl'
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        particles={test_key2: test_value2}
    )
    graphics.add_particles({test_key1: test_value1})
    assert graphics._particle_obj[test_key1] == test_value1
    assert graphics._particle_obj[test_key2] == test_value2


def test_add_animate_list_none_existing():
    test_list = ['walk']
    graphics = EntityGraphics(_test_namespace, _test_id)
    graphics.add_animate_list(test_list)
    assert graphics._animate_list == test_list


def test_add_animate_list_existing_anims():
    test_value1 = 'walk'
    test_value2 = 'attack'
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        animate_list=[test_value1]
    )
    graphics.add_animate_list([test_value2])
    assert test_value1 in graphics._animate_list
    assert test_value2 in graphics._animate_list


def test_add_script_init_none_existing():
    test_list = ['v.test = 0;']
    graphics = EntityGraphics(_test_namespace, _test_id)
    graphics.add_script_initialize(test_list)
    assert graphics.init_list == test_list


def test_add_script_init_existing_values():
    test_value1 = 'v.test1 = 0;'
    test_value2 = 'v.test2 = 10;'
    graphics = EntityGraphics(_test_namespace, _test_id)
    graphics.add_script_initialize([test_value1])
    graphics.add_script_initialize([test_value2])
    assert test_value1 in graphics.init_list
    assert test_value2 in graphics.init_list


def test_add_script_pre_anim_none_existing():
    test_list = ['v.test = 0;']
    graphics = EntityGraphics(_test_namespace, _test_id)
    graphics.add_script_pre_anim(test_list)
    assert graphics.pre_anim == test_list


def test_add_script_pre_anim_existing_values():
    test_value1 = 'v.test1 = 0;'
    test_value2 = 'v.test2 = 10;'
    graphics = EntityGraphics(_test_namespace, _test_id)
    graphics.add_script_pre_anim([test_value1])
    graphics.add_script_pre_anim([test_value2])
    assert test_value1 in graphics.pre_anim
    assert test_value2 in graphics.pre_anim


def test_add_ranco_anims():
    test_value = 'controller.animation.test_entity'
    anco = AnimationController(test_value)
    graphics = EntityGraphics(_test_namespace, _test_id)
    graphics.add_ranco(anco)
    assert graphics._anim_obj[test_value] == test_value


def test_add_ranco_animate_list():
    test_value = 'controller.animation.test_entity'
    anco = AnimationController(test_value)
    graphics = EntityGraphics(_test_namespace, _test_id)
    graphics.add_ranco(anco)
    assert test_value in graphics._animate_list


def test_json_has_format_version():
    graphics = EntityGraphics(_test_namespace, _test_id)
    assert 'format_version' in graphics.get_json()


def test_json_has_entity():
    graphics = EntityGraphics(_test_namespace, _test_id)
    assert 'minecraft:client_entity' in graphics.get_json()


def test_json_has_description():
    graphics = EntityGraphics(_test_namespace, _test_id)
    entity = graphics.get_json()['minecraft:client_entity']
    assert 'description' in entity


def test_json_material():
    test_value = 'test_material'
    graphics = EntityGraphics(_test_namespace, _test_id, material=test_value)
    desc = graphics.get_json()['minecraft:client_entity']['description']
    assert desc['materials'] == {'default': test_value}


def test_json_renco():
    test_value = 'test_renco'
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        render_controller=test_value
    )
    desc = graphics.get_json()['minecraft:client_entity']['description']
    assert desc['render_controllers'] == [test_value]


def test_json_geo_single():
    test_value = 'test'
    graphics = EntityGraphics(_test_namespace, _test_id, geo=test_value)
    desc = graphics.get_json()['minecraft:client_entity']['description']
    assert desc['geometry'] == {'default': f'geometry.{test_value}'}


def test_json_geo_multiple():
    input_values = {
        'main': 'main_geo',
        'other': 'other_geo'
    }
    expected_values = {
        'main': 'geometry.main_geo',
        'other': 'geometry.other_geo'
    }
    graphics = EntityGraphics(_test_namespace, _test_id, geo=input_values)
    desc = graphics.get_json()['minecraft:client_entity']['description']
    assert desc['geometry'] == expected_values


def test_json_tex_single():
    test_value = 'test'
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        texture_path=test_value
    )
    desc = graphics.get_json()['minecraft:client_entity']['description']
    assert desc['textures'] == {'default': f'textures/entity/{test_value}'}


def test_json_tex_multiple():
    input_values = {
        'main': 'main_tex',
        'other': 'other_tex'
    }
    expected_values = {
        'main': 'textures/entity/main_tex',
        'other': 'textures/entity/other_tex'
    }
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        texture_path=input_values
    )
    desc = graphics.get_json()['minecraft:client_entity']['description']
    assert desc['textures'] == expected_values


def test_json_invisible_material():
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        invisible=True
    )
    desc = graphics.get_json()['minecraft:client_entity']['description']
    assert 'material' not in desc


def test_json_invisible_tex():
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        invisible=True
    )
    desc = graphics.get_json()['minecraft:client_entity']['description']
    assert 'textures' not in desc


def test_json_invisible_geo():
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        invisible=True
    )
    desc = graphics.get_json()['minecraft:client_entity']['description']
    assert desc['geometry'] == {'default': 'geometry.humanoid'}


def test_json_spawn_egg():
    test_value1 = '#00ff00'
    test_value2 = '#888888'
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        egg_color_1=test_value1,
        egg_color_2=test_value2
    )
    desc = graphics.get_json()['minecraft:client_entity']['description']
    assert desc['spawn_egg'] == {
        'base_color': test_value1,
        'overlay_color': test_value2
    }


def test_json_animations():
    test_values = {'anim_name': 'animation.anim_id'}
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        animations=test_values
    )
    desc = graphics.get_json()['minecraft:client_entity']['description']
    assert desc['animations'] == test_values


def test_json_particles():
    test_values = {'particle_name': 'particle_id'}
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        particles=test_values
    )
    desc = graphics.get_json()['minecraft:client_entity']['description']
    assert desc['particle_effects'] == test_values


def test_json_scale():
    input_value = 2.0
    expected_output = '2.0'
    graphics = EntityGraphics(
        _test_namespace,
        _test_id
    )
    graphics.scale = input_value
    desc = graphics.get_json()['minecraft:client_entity']['description']
    scripts = desc['scripts']
    assert scripts['scale'] == expected_output


def test_json_animate_list():
    test_values = ['walk']
    graphics = EntityGraphics(
        _test_namespace,
        _test_id,
        animate_list=test_values
    )
    desc = graphics.get_json()['minecraft:client_entity']['description']
    scripts = desc['scripts']
    assert scripts['animate'] == test_values


def test_json_initialize():
    test_values = ['v.test = 0;']
    graphics = EntityGraphics(
        _test_namespace,
        _test_id
    )
    graphics.init_list = test_values
    desc = graphics.get_json()['minecraft:client_entity']['description']
    scripts = desc['scripts']
    assert scripts['initialize'] == test_values


def test_json_pre_animation():
    test_values = ['v.test = 0;']
    graphics = EntityGraphics(
        _test_namespace,
        _test_id
    )
    graphics.pre_anim = test_values
    desc = graphics.get_json()['minecraft:client_entity']['description']
    scripts = desc['scripts']
    assert scripts['pre_animation'] == test_values
