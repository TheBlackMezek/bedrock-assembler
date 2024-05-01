from brockassemble.command import selector


def test_no_optional_parameters():
    assert selector('e') == '@e'


def test_one_tag():
    assert selector('e', tags=['tag1']) == '@e[tag=tag1]'


def test_multiple_tags():
    result = selector('e', tags=['tag1', 'tag2', 'tag3'])
    assert result == '@e[tag=tag1,tag=tag2,tag=tag3]'


def test_not_tag():
    assert selector('e', not_tags=['tag1']) == '@e[tag=!tag1]'


def test_radius():
    assert selector('e', radius=5) == '@e[r=5]'


def test_max_selected():
    assert selector('e', max_selected=5) == '@e[c=5]'


def test_x():
    assert selector('e', x=1) == '@e[x=1]'


def test_y():
    assert selector('e', y=1) == '@e[y=1]'


def test_z():
    assert selector('e', z=1) == '@e[z=1]'


def test_dx():
    assert selector('e', dx=1) == '@e[dx=1]'


def test_dy():
    assert selector('e', dy=1) == '@e[dy=1]'


def test_dz():
    assert selector('e', dz=1) == '@e[dz=1]'


def test_rotation_x():
    assert selector('e', rotation_x=1) == '@e[rx=1]'


def test_rotation_y():
    assert selector('e', rotation_y=1) == '@e[ry=1]'


def test_xp_lvl_min():
    assert selector('e', xp_lvl_min=1) == '@e[lm=1]'


def test_xp_lvl_max():
    assert selector('e', xp_lvl_max=1) == '@e[l=1]'


def test_gamemode():
    assert selector('e', gamemode='s') == '@e[m=s]'


def test_not_gamemode():
    assert selector('e', not_gamemode='s') == '@e[m=!s]'


def test_name():
    assert selector('e', name='fido') == '@e[name=fido]'


def test_not_name_single():
    assert selector('e', not_names=['fido']) == '@e[name=!fido]'


def test_not_name_multiple():
    result = selector('e', not_names=['fido', 'spot', 'stinky'])
    assert result == '@e[name=!fido,name=!spot,name=!stinky]'


def test_entity_id():
    result = selector('e', entity_id='custom:test_mob')
    assert result == '@e[type=custom:test_mob]'


def test_not_entity_ids():
    result = selector('e', not_entity_ids=[
        'custom:test_mob',
        'custom:test_mob2'
    ])
    assert result == '@e[type=!custom:test_mob,type=!custom:test_mob2]'


def test_families():
    result = selector('e', families=[
        'mob',
        'monster'
    ])
    assert result == '@e[family=mob,family=monster]'


def test_not_families():
    result = selector('e', not_families=[
        'mob',
        'monster'
    ])
    assert result == '@e[family=!mob,family=!monster]'
