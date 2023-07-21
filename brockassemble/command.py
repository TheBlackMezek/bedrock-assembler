

def selector(base_selector: str,
             tags: list = None,
             not_tags: list = None,
             radius: float = None,
             max_selected: int = None,
             x: float = None,
             y: float = None,
             z: float = None,
             dx: float = None,
             dy: float = None,
             dz: float = None,
             rotation_x: float = None,
             rotation_y: float = None,
             xp_lvl_min: int = None,
             xp_lvl_max: int = None,
             gamemode: str = None,
             not_gamemode: str = None,
             name: str = None,
             not_names: list = None,
             entity_id: str = None,
             not_entity_ids: list = None,
             families: list = None,
             not_families: list = None) -> str:
    '''Base selector can be any of the following: a, p, s, e, r'''

    s = '@'+base_selector

    params = []

    if tags is not None:
        for t in tags:
            params.append('tag='+t)
    if not_tags is not None:
        for t in not_tags:
            params.append('tag=!'+t)
    if radius is not None:
        params.append(f'r={radius}')
    if max_selected is not None:
        params.append(f'c={max_selected}')
    if x is not None:
        params.append(f'x={x}')
    if y is not None:
        params.append(f'y={y}')
    if z is not None:
        params.append(f'z={z}')
    if dx is not None:
        params.append(f'dx={dx}')
    if dy is not None:
        params.append(f'dy={dy}')
    if dz is not None:
        params.append(f'dz={dz}')
    if rotation_x is not None:
        params.append(f'rx={rotation_x}')
    if rotation_y is not None:
        params.append(f'ry={rotation_y}')
    if xp_lvl_min is not None:
        params.append(f'lm={xp_lvl_min}')
    if xp_lvl_max is not None:
        params.append(f'l={xp_lvl_max}')
    if gamemode is not None:
        params.append(f'm={gamemode}')
    if not_gamemode is not None:
        params.append(f'm=!{not_gamemode}')
    if name is not None:
        params.append(f'name={name}')
    if not_names is not None:
        for n in not_names:
            params.append('name=!'+n)
    if entity_id is not None:
        params.append(f'type={entity_id}')
    if not_entity_ids is not None:
        for d in not_entity_ids:
            params.append('type=!'+d)
    if families is not None:
        for f in families:
            params.append('family='+f)
    if not_families is not None:
        for f in not_families:
            params.append('family=!'+f)

    if len(params) > 0:
        s += '['
        for p in params:
            s += p + ','
        s = s.rstrip(s[-1])
        s += ']'

    return s


def command_base(cmd: str,
                 selector: str = None,
                 include_slash: bool = True) -> str:
    '''For internal command_builder use'''
    ret = ''
    if include_slash:
        ret += '/'
    ret += cmd
    if selector is not None:
        ret += ' '+selector
    return ret


def execute(cmd: str,
            selector: str = None,
            x: str = '~',
            y: str = '~',
            z: str = '~',
            include_slash: bool = True,
            detect_block: str = None,
            detect_data_id: int = 0,
            detect_x: str = '~',
            detect_y: str = '~',
            detect_z: str = '~') -> str:
    '''All position arguments can also be floats'''
    ret = command_base('execute', selector, include_slash)
    ret += f' {x} {y} {z}'
    if detect_block is not None:
        ret += ' detect'
        ret += f' {detect_x} {detect_y} {detect_z}'
        ret += ' '+detect_block
        ret += f' {detect_data_id}'
    ret += ' '+cmd
    # Use the below code when Mojank implements the new /execute syntax for things other than the player
    # Also, replace the default '~' for x, y, z with None
    # ret = command_base('execute', None, include_slash)
    # if selector is not None:
    #     ret += ' as '+selector
    # if x is not None:
    #     ret += f' positioned {x} {y} {z}'
    # if detect_block is not None:
    #     ret += ' if block'
    #     ret += f' {detect_x} {detect_y} {detect_z}'
    #     ret += ' '+detect_block
    #     ret += f' {detect_data_id}'
    # ret += ' run '+cmd
    return ret


def tp(victim_selector: str = None,
       x: str = None,
       y: str = None,
       z: str = None,
       target_selector: str = None,
       x_rot: float = None,
       y_rot: float = None,
       facing_selector: str = None,
       facing_x: str = None,
       facing_y: str = None,
       facing_z: str = None,
       check_for_blocks: bool = False,
       include_slash: bool = True) -> str:
    '''Must be supplied EITHER with target_selector or x y z\n
       Use one at most of: y_rot & x_rot; facing_selector; facing_x y z\n
       check_for_blocks checks if destination has only nonsolid blocks\n
       All position arguments can also be floats'''
    ret = command_base('tp', include_slash=include_slash)

    if victim_selector is not None:
        ret += ' '+victim_selector

    if target_selector is not None:
        ret += ' '+target_selector
    else:
        ret += f' {x} {y}{ z}'

    if x_rot is not None:
        ret += f' {x_rot} {y_rot}'
    elif facing_selector is not None:
        ret += ' '+facing_selector
    elif facing_x is not None:
        ret += f' {facing_x} {facing_y} {facing_z}'

    if check_for_blocks:
        ret += ' true'

    return ret


def effect(selector: str,
           effect: str = None,
           duration: float = 1.0,
           level: int = 1,
           hide_particles: bool = False,
           clear: bool = False,
           include_slash: bool = True):
    '''If clear==True, all other parameters will be ignored'''
    ret = command_base('effect', selector, include_slash)
    if clear:
        ret += ' clear'
        return ret
    ret += ' '+effect
    ret += f' {duration}'
    ret += f' {level}'
    if hide_particles:
        ret += ' true'
    return ret


def summon(entity_id: str,
           name: str = None,
           x: str = None,
           y: str = None,
           z: str = None,
           spawn_event: str = None,
           include_slash: bool = True):
    '''Make sure you provide coordinates if using spawn_event!'''
    ret = command_base('summon', entity_id, include_slash)

    if spawn_event is not None or name is None:
        if x is not None:
            ret += f' {x} {y} {z}'
        if spawn_event is not None:
            ret += ' '+spawn_event
        if name is not None:
            ret += f' "{name}"'
    else:
        ret += f' "{name}"'
        if x is not None:
            ret += f' {x} {y} {z}'

    return ret


def tag(selector: str,
        tag_id: str = None,
        mode_add: bool = False,
        mode_remove: bool = False,
        mode_list: bool = False,
        include_slash: bool = True) -> str:
    '''Set EXACTLY ONE mode argument to True\n
       tag_id will not be used if mode_list==True'''
    ret = command_base('tag', selector, include_slash)
    if mode_add:
        ret += ' add '+tag_id
    elif mode_remove:
        ret += ' remove '+tag_id
    elif mode_list:
        ret += ' list'

    return ret


def summon_rider(target_selector: str,
                 rider_type: str,
                 spawn_event: str = None,
                 nametag: str = None,
                 include_slash: bool = True) -> str:
    '''If using nametag, you MUST include spawn_event\n
       For most mobs, spawn_event should be "minecraft:entity_spawned"'''
    ret = command_base('ride', target_selector, include_slash)
    ret += ' summon_rider'
    ret += ' '+rider_type
    if spawn_event is not None:
        ret += ' '+spawn_event
        if nametag is not None:
            ret += f' "{nametag}"'
    return ret


def event(selector: str,
          event_name: str,
          include_slash: bool = True) -> str:
    ret = command_base('event entity', selector, include_slash)
    ret += ' '+event_name
    return ret


def kill(selector: str,
         include_slash: bool = True) -> str:
    return command_base('kill', selector, include_slash)
