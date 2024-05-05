from brockassemble.entity import AnimationFile, Animation


def test_format_version():
    test_value = "1.1.0"
    af = AnimationFile()
    af.format_version = test_value
    assert af.get_json()['format_version'] == test_value


def test_anim_ids():
    test_value = 'animation.test_anim'
    anim = Animation(test_value)
    af = AnimationFile([anim])
    assert test_value in af.get_json()['animations'].keys()


def test_add_anim():
    test_value = 'animation.test_anim'
    anim = Animation(test_value)
    af = AnimationFile()
    af.add_anim(anim)
    assert test_value in af.get_json()['animations'].keys()


def test_add_anims():
    test_value1 = 'animation.test_anim_1'
    test_value2 = 'animation.test_anim_2'
    anim1 = Animation(test_value1)
    anim2 = Animation(test_value2)
    af = AnimationFile()
    af.add_anims([anim1, anim2])
    assert test_value1 in af.get_json()['animations'].keys()
    assert test_value2 in af.get_json()['animations'].keys()
