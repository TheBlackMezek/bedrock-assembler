"""
Module containing functions for generating in-game commands
and elements of commands.
"""

def selector(
        base_selector: str,
        tags: list[str] = None,
        not_tags: list[str] = None,
        radius: float = None,
        max_selected: int = None,
        x: float = None,
        y: float = None,
        z: float = None,
        dx: float = None,
        dy: float = None,
        dz: float = None,
        rotation_x: float | str = None,
        rotation_y: float | str = None,
        xp_lvl_min: int = None,
        xp_lvl_max: int = None,
        gamemode: str | int = None,
        not_gamemode: str | int = None,
        name: str = None,
        not_names: list[str] = None,
        entity_id: str = None,
        not_entity_ids: list[str] = None,
        families: list[str] = None,
        not_families: list[str] = None) -> str:
    """
    Creates a target selector.

    Parameters
    ----------
    base_selector : str
        The root of the target selector. Valid characters are:
        a (all players),
        p (nearest player),
        s (self),
        e (all entities, add further conditions to this or it can cause lag),
        r (random player)
    tags : list[str]
        A list of tags which must all be present on the target entity.
    not_tags : list[str]
        A list of tags which must all be absent from the target entity.
    radius : float
        The maximum distance target entities can be from the command origin.
    max_selected : int
        The maximum number of entities which can be selected.
        Will prioritize entities closer to the command origin.
    x, y, z : float
        Coordinates for the command origin, which can be in absolute
        coordinates or relative tilde '~' coordinates.
        It cannot be in relative caret '^' coordinates.
    dx, dy, dz : float
        Dimensions of a bounding box which selected entities must be within.
        If used with the x, y, z parameters, they set the corner of the box
        which dx, dy, dz stretch out from. For example, x=10 and dx=5 would
        create a bounding box with X axis boundaries of 10 and 15. Otherwise,
        command caller's position is used. 
    rotation_x, rotation_y : float | str
        Specify the direction the entity must be facing.
        Can be given as a specific value (x_rotation=50)
        or a range (x_rotation='30..60').
        Values for x_rotation (vertical) range from -90 (straight up) to
        90 (straight down).
        Values for y_rotation (horizontal) range from -180 (north)
        to -90 (east) to 0 (south) to 90 (west) to 180 (north again).
    xp_level_min : int
        Minimum XP level for the target entity.
    xp_level_max : int
        Maximum XP level for the target entity.
    gamemode : str | int
        Gamemode requirement for the target. Only useful for players.
        Possible values are 'spectator', 'survival', 'creative',
        and 'adventure'. Acceptable shorthand values are 's' or 0 for survival,
        'c' or 1 for creative, and 'a' or 2 for adventure.
    not_gamemode : str | int
        Requirement that the target is not in this gamemode. Only useful for
        players. Accepts same possible values as previously listed for the
        gamemode parameter.
    name : str
        The name the target must have. Non-player entities have a default
        name value, which can be altered with commands and nametags.
        Distinct from entity ID, which cannot be changed in-game.
    not_names : list[str]
        Names which the targets must not have.
    entity_id : str
        The specific class of entity to target. Don't forget to include the
        namespace.
    not_entity_ids : list[str]
        The specific classes of entity not to target.
    families : list[str]
        The entity families the targets must belong to.
    not_families : list[str]
        The entity families the targets must not belong to.

    Returns
    -------
    str
        A target selector which can be used in an in-game command.
    """

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


def _command_stem(
        cmd: str,
        selector: str = None,
        include_slash: bool = True) -> str:
    """
    Creates a command string stem which command parameters can be added to.

    Parameters
    ----------
    cmd : str
        The name of the command, such as 'tp' or 'summon'.
    selector : str
        The target selector, such as '@e[r=10]'.
    include_slash : bool
        Whether or not the command begins with a forward slash '/'. This is
        necessary for some cases but will break others.
    
    Returns
    -------
    str
        The fully assembled command stem.
        Example: '/tp @e[r=10]'.
    """
    ret = ''
    if include_slash:
        ret += '/'
    ret += cmd
    if selector is not None:
        ret += ' '+selector
    return ret


def execute(
        cmd: str,
        selector: str = None,
        x: str | float = '~',
        y: str | float = '~',
        z: str | float = '~',
        include_slash: bool = True,
        detect_block: str = None,
        detect_data_id: int = 0,
        detect_x: str | float = '~',
        detect_y: str | float = '~',
        detect_z: str | float = '~') -> str:
    """
    Wraps a command inside of an execute command.

    Parameters
    ----------
    cmd : str
        The command which will be wrapped inside /execute.
    selector : str
        The target selector for this command.
    x, y, z : str | float
        The position to execute the command from.
        If floats, will use absolute coordinates.
        If strings, can use relative coordinates with tilde '~' notation.
    include_slash : bool
        Whether or not the command begins with a forward slash '/'. This is
        necessary for some cases but will break others.
    detect_block : str
        The ID of a block which must be detected at the detection coordinates
        for the command to execute.
    detect_data_id : int
        The additional data value of the block to be detected.
    detect_x, detect_y, detect_z : str | float
        The position at which to check for the block type.
        If floats, will use absolute coordinates.
        If strings, can use relative coordinates with tilde '~' notation.
    
    Returns
    -------
    str
        A complete /execute command.
        Example: '/execute @e[r=10] ~ ~ ~ summon pig'.
    """
    ret = _command_stem('execute', selector, include_slash)
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


def tp(
        victim_selector: str = None,
        x: str | float = None,
        y: str | float = None,
        z: str | float = None,
        target_selector: str = None,
        x_rot: float = None,
        y_rot: float = None,
        facing_selector: str = None,
        facing_x: str | float = None,
        facing_y: str | float = None,
        facing_z: str | float = None,
        check_for_blocks: bool = False,
        include_slash: bool = True) -> str:
    """
    Creates a teleport command.

    Use one at most of: y_rot & x_rot; facing_selector; facing_x y z\n
    check_for_blocks checks if destination has only nonsolid blocks\n
    All position arguments can also be floats

    Parameters
    ----------
    victim_selector : str
        The target selector for the entities to be teleported.
    x, y, z : str | float
        Coordinates to teleport the victims to.
        If floats, will use absolute coordinates.
        If strings, can use relative coordinates with tilde '~' notation.
        INCOMPATIBLE with use of target_selector parameter.
    target_selector : str
        A target selector for the destination entity the victims will be
        teleported to.
        INCOMPATIBLE with use of x, y, z parameters.
    x_rot, y_rot : float
        The X and Y rotation victim entities will have after teleportation.
        INCOMPATIBLE with use of facing_selector and
        facing_x, _y, _z parameters.
    facing_selector : str
        Target selector for an entity the victims will turn to face after
        teleportation.
        INCOMPATIBLE with use of x_rot, y_rot, and facing_x, _y, _z parameters.
    facing_x, facing_y, facing_z : str | float
        Coordinates which the victim entities will face after teleportation.
        If floats, will use absolute coordinates.
        If strings, can use relative coordinates with tilde '~' notation.
        INCOMPATIBLE with use of x_rot, y_rot, and facing_selector parameters.
    check_for_blocks : bool
        If true, victims will not be teleported if target position is inside a
        solid block.
    include_slash : bool
        Whether or not the command begins with a forward slash '/'. This is
        necessary for some cases but will break others.
    
    Returns
    -------
    str
        A complete /tp command.
        Example: '/tp @e[r=10] 23 56 998 facing ~ ~1 ~5 true'.
    """
    ret = _command_stem('tp', include_slash=include_slash)

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


def effect(
        selector: str,
        effect: str = None,
        duration: float = 1.0,
        level: int = 1,
        hide_particles: bool = False,
        clear: bool = False,
        include_slash: bool = True) -> str:
    """
    Creates an effect command, which applies a potion effect to one
    or more entities.

    Parameters
    ----------
    selector : str
        The target selector for the entities which will have the effect
        applied to them.
    effect : str
        The ID of the potion effect to apply.
    duration : float
        How long the effect will last.
        This will not do anything to instantaneous effects,
        such as instant_health.
    level : int
        The intensity level of the effect.
        How this is applied varies depending on the effect.
    hide_particles : bool
        If True, the swirly potion particles which normally are emitted by
        an entity with a potion effect are not emitted.
    clear : bool
        If True, removes all potion effects from the entity.
        Additionally, if True, the effect, duration, level, and hide_particles
        parameters will be ignored.
    include_slash : bool
        Whether or not the command begins with a forward slash '/'. This is
        necessary for some cases but will break others.
    
    Returns
    -------
    str
        A complete /effect command.
        Example: '/effect @s regeneration 60 5 true'.
    """
    ret = _command_stem('effect', selector, include_slash)
    if clear:
        ret += ' clear'
        return ret
    ret += ' '+effect
    ret += f' {duration}'
    ret += f' {level}'
    if hide_particles:
        ret += ' true'
    return ret


def summon(
        entity_id: str,
        name: str = None,
        x: str | float = None,
        y: str | float = None,
        z: str | float = None,
        spawn_event: str = None,
        include_slash: bool = True) -> str:
    """
    Creates a command to summon an entity.

    Parameters
    ----------
    entity_id : str
        The ID of the entity to be summoned.
    x, y, z : str | float
        The position to summon the entity at.
        If not provided, the entity will be summoned at
        the summoner's position.
        If floats, will use absolute coordinates.
        If strings, can use relative coordinates with tilde '~' notation.
    spawn_event : str
        The specific event to be called on the entity when it spawns.
        If not provided, the Bedrock default is 'minecraft:entity_spawned'.
        If you use spawn_event, you MUST also provide x, y, z.
    include_slash : bool
        Whether or not the command begins with a forward slash '/'. This is
        necessary for some cases but will break others.

    Returns
    -------
    str
        A complete /summon command.
        Example: '/summon pig ~10 ~ ~'
    """
    ret = _command_stem('summon', entity_id, include_slash)

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


def tag(
        selector: str,
        tag_id: str = None,
        mode_add: bool = False,
        mode_remove: bool = False,
        mode_list: bool = False,
        include_slash: bool = True) -> str:
    """
    Creates a command which adds, removes, or lists tags on an entity.
    Set EXACTLY ONE mode_ parameter to True.

    Parameters
    ----------
    selector : str
        The target selector for the entities to operate upon.
    tag_id : str
        The tag to be added or removed. Has no effect if using mode_list.
    mode_add : bool
        If true, creates a command to add a tag to the target entities.
    mode_remove : bool
        If true, creates a command to remove a tag from the target entities.
    mode_list : bool
        If true, prints a list of all tags currently on the target entities.
    include_slash : bool
        Whether or not the command begins with a forward slash '/'. This is
        necessary for some cases but will break others.
    
    Returns
    -------
    str
        A complete /tag command.
        Example: '/tag @e[r=10] add marked_for_explode'
    """
    ret = _command_stem('tag', selector, include_slash)
    if mode_add:
        ret += ' add '+tag_id
    elif mode_remove:
        ret += ' remove '+tag_id
    elif mode_list:
        ret += ' list'

    return ret


def summon_rider(
        target_selector: str,
        rider_type: str,
        spawn_event: str = None,
        nametag: str = None,
        include_slash: bool = True) -> str:
    """
    Creates a command which summons a rider onto selected entities.

    Parameters
    ----------
    target_selector : str
        The target selector for the entities to summon riders on.
    rider_type : str
        The entity ID of the riders to be summoned.
    spawn_event : str
        The specific event to be called on the riders when they spawn.
        If not provided, the Bedrock default is 'minecraft:entity_spawned'.
    nametag : str
        A name to be given to the summoned riders.
        If you use the nametag parameter, you MUST also use spawn_event,
        even if you're just using the default 'minecraft:entity_spawned'.
    include_slash : bool
        Whether or not the command begins with a forward slash '/'. This is
        necessary for some cases but will break others.
    
    Returns
    -------
    str
        A complete summon rider command.
        Example: '/ride @e[type=boat,r=20] summon_rider pig'
    """
    ret = _command_stem('ride', target_selector, include_slash)
    ret += ' summon_rider'
    ret += ' '+rider_type
    if spawn_event is not None:
        ret += ' '+spawn_event
        if nametag is not None:
            ret += f' "{nametag}"'
    return ret


def event(
        selector: str,
        event_name: str,
        include_slash: bool = True) -> str:
    """
    Creates a command which calls an event on selected entities.

    Parameters
    ----------
    selector : str
        The target selector for the entities to call the event on.
    event_name : str
        The ID of the event to be called.
    include_slash : bool
        Whether or not the command begins with a forward slash '/'. This is
        necessary for some cases but will break others.
    
    Returns
    -------
    str
        A complete event command.
        Example: '/event entity @e[type=myteam:jump_pad] myteam:activate_jump'
    """
    ret = _command_stem('event entity', selector, include_slash)
    ret += ' '+event_name
    return ret


def kill(selector: str,
         include_slash: bool = True) -> str:
    return _command_stem('kill', selector, include_slash)
