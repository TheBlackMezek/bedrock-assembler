"""
Module containing the Component class and functions for generating various
entity components.
"""
from brockassemble.exceptions import MissingParameterError


class Component:
    """
    Base class for any addon file which uses a component system.
    This includes entity behavior files, item behavior files, and particles.

    Attributes
    ----------
    comp_type : str
    json_obj : dict
    """

    def __init__(self, type: str, priority: int = None):
        """
        Parameters
        ----------
        type : str
            The component type ID. Must be a valid type for the component
            system you're using.
        priority : int
            The priority of following this component compared to all others
            currently active. Lower numbers are higher priority, with 0 being
            highest priority.
        """

        self.json_obj: dict = {}
        """The JSON-writable body of the component."""

        self.comp_type: str = type
        """
        The component type ID. Must be a valid type for the component system
        you're using.
        """

        if priority is not None:
            self.json_obj['priority'] = priority

    def get_id(self) -> str:
        """This entity's type prefixed with the 'minecraft:' namespace."""
        return 'minecraft:' + self.comp_type


def component_family(families: list[str]) -> Component:
    """
    Creates a type_family component.\n
    type_family has no effects on its own, but can be used by filters to detect
    certain types of entities.

    Parameters
    ----------
    families : list[str]
        All of the families the entity will belong to.

    Returns
    -------
    Component
        A type_family Component.
    """
    comp = Component('type_family')
    comp.json_obj['family'] = families
    return comp


def component_timer(length: float, event: str) -> Component:
    """
    Creates a timer component.\n
    There can only be one active timer component at once in an entity.

    Parameters
    ----------
    length : float
        Duration that the timer will run for.
    event : str
        The event to call in the entity when the timer runs out.

    Returns
    -------
    Component
        A timer Component.
    """
    comp = Component('timer')
    comp.json_obj['randomInterval'] = False
    comp.json_obj['time'] = length
    comp.json_obj['time_down_event'] = {'event': event}
    return comp


def component_skin_id(skin_id: int) -> Component:
    """
    Creates a skin_id component.\n
    Skin_id is useful for sending data between entity files,
    but entity properties are generally preferable.

    Parameters
    ----------
    skin_id : int
        The skin ID number.

    Returns
    -------
    Component
        A skin_id Component.
    """
    comp = Component('skin_id')
    comp.json_obj['value'] = skin_id
    return comp


def component_variant(variant: int) -> Component:
    """
    Creates a variant component.\n
    Variant is useful for sending data between entity files,
    but entity properties are generally preferable.

    Parameters
    ----------
    variant : int
        The variant ID number.

    Returns
    -------
    Component
        A variant Component.
    """
    comp = Component('variant')
    comp.json_obj['value'] = variant
    return comp


def component_mark_variant(mark_variant: int) -> Component:
    """
    Creates a mark_variant component.\n
    Mark_variant is useful for sending data between entity files,
    but entity properties are generally preferable.

    Parameters
    ----------
    mark_variant : int
        The mark_variant ID number.

    Returns
    -------
    Component
        A mark_variant Component.
    """
    comp = Component('mark_variant')
    comp.json_obj['value'] = mark_variant
    return comp


def component_scale(scale: float) -> Component:
    """
    Creates a scale component.\n
    Scale multiplies the entity's visual size and hitbox.
    It can have some weird effects, so it's best to make the model at the
    desired size to begin with, and to set the hitbox size directly.

    Parameters
    ----------
    scale : float
        The number to multiply the entity's visual size and hitbox by.

    Returns
    -------
    Component
        A scale Component.
    """
    comp = Component('scale')
    comp.json_obj['value'] = scale
    return comp


def component_movement(speed: float) -> Component:
    """
    Creates a movement component.\n
    This sets an entity's walkspeed, which can be further modified under
    certain conditions by other components.

    Parameters
    ----------
    speed : float
        The walkspeed the entity will have.

    Returns
    -------
    Component
        A movement Component.
    """
    comp = Component('movement')
    comp.json_obj['value'] = speed
    return comp


def component_stroll(
        speed: float = 1.0,
        priority: int = 5) -> Component:
    """
    Creates a behavior.random_stroll component.\n
    This behavior component causes the entity to wander around randomly.

    Parameters
    ----------
    speed : float
        A number to multiply the entity's default walkspeed by while wandering.
    priority : int
        The priority of this behavior in the entity compared to other
        behaviors. Lower numbers are higher priority.

    Returns
    -------
    Component
        A behavior.random_stroll Component.
    """
    comp = Component('behavior.random_stroll', priority=priority)
    comp.json_obj['speed_multiplier'] = speed
    return comp


def component_random_look(priority: int = 8) -> Component:
    """
    Creates a behavior.random_look_around component.\n
    This behavior component causes the entity to periodically rotate its head
    and body in a random direction.

    Parameters
    ----------
    priority : int
        The priority of this behavior in the entity compared to other
        behaviors. Lower numbers are higher priority.

    Returns
    -------
    Component
        A behavior.random_look_around Component.
    """
    return (Component('behavior.random_look_around', priority=priority))


def component_attack(
        dmg: int | list[int],
        effect_id: str = None,
        effect_duration: float = None) -> Component:
    """
    Creates an attack component.\n
    This component sets the properties of an entity's melee attack.
    It does create targeting or movement to make attacks actually happen.\n

    Parameters
    ----------
    dmg : int | list[int]
        The amount of damage the entity does each attack. 1 damage is equal to
        half a heart.
        If using a list, the amount of damage will be random, where dmg[0] is
        the minimum damage and dmg[1] is the maximum damage.
    effect_id : str
        The ID of a potion effect to apply to the target on hit.
        effect_duration must also be given if you use effect_id.
    effect_duration : float
        The length of time the potion effect will last, in seconds.

    Returns
    -------
    Component
        An attack Component.
    """
    comp = Component('attack')
    comp.json_obj['damage'] = dmg
    if (effect_id, effect_duration).count(None) == 1:
        raise MissingParameterError(
            "Either 'effect_id' and 'effect_duration' must both be used, "
            "OR they must both be None"
        )
    else:
        comp.json_obj['effect_name'] = effect_id
        comp.json_obj['effect_duration'] = effect_duration
    return comp


def component_melee_attack(
        speed_multiplier: float = None,
        track_target: bool = None,
        reach_multiplier: float = None) -> Component:
    """
    Creates a behavior.melee_attack component.\n
    This component causes the entity to move towards its target and do melee
    attacks. The entity must also have an "attack" component to define stats
    like melee damage, and a targeting component such as
    behavior.nearest_attackable_target.

    Parameters
    ----------
    speed_multiplier : float
        A number to multiply the entity's default walkspeed by while moving
        to attack.
    track_target : bool
        If true, allows the entity to track its target even if it doesn't have
        any sensing.
    reach_multiplier : float
        The melee attack range, muliplied from the entity's base size. If not
        supplied, the Bedrock default value is 2.0.

    Returns
    -------
    Component
        A behavior.melee_attack Component.
    """
    comp = Component('behavior.melee_attack')
    if speed_multiplier is not None:
        comp.json_obj['speed_multiplier'] = speed_multiplier
    if track_target is not None:
        comp.json_obj['track_target'] = track_target
    if reach_multiplier is not None:
        comp.json_obj['reach_multiplier'] = reach_multiplier
    return comp


def component_ranged_attack(
        attack_range: float = 15.0,
        interval_min: float = 1.0,
        interval_max: float = 3.0) -> Component:
    """
    Creates a behavior.ranged_attack component.\n
    This component causes the entity to approach its target and shoot
    projectiles at them.

    Parameters
    ----------
    attack_range : float
        The minimum distance between the entity and its target before the
        entity will shoot. When beyond this range, the entity will try to
        get close to its target.
    interval_min : float
        Minimum time between shots. Randomized between interval_max.
    interval_max : float
        Maximum time between shots. Randomized between interval_min.

    Returns
    -------
    Component
        A behavior.ranged_attack Component.
    """
    comp = Component('behavior.ranged_attack')
    comp.json_obj = {
        "attack_radius": attack_range,
        "attack_interval_min": interval_min,
        "attack_interval_max": interval_max
    }
    return comp


def component_area_attack(
        range: float,
        dmg: int) -> Component:
    """
    Creates an area_attack component.\n
    This component deals damage to every entity within range every tick.

    Parameters
    ----------
    range : float
        The maximum range of the attack.
    dmg : int
        How much damage is done every tick. 1 point is 1/2 heart.

    Returns
    -------
    Component
        An area_attack Component.
    """
    comp = Component('area_attack')
    comp.json_obj['damage_range'] = range
    comp.json_obj['damage_per_tick'] = dmg
    return comp


def component_health(max_hp: int):
    """
    Creates a health component.\n
    This sets the entity's max health. It is necessary for most mobs.

    Parameters
    ----------
    max_hp : int
        The entity's maximum health. 1 point is 1/2 heart.

    Returns
    -------
    Component
        A health Component.
    """
    comp = Component('health')
    comp.json_obj['max'] = max_hp
    comp.json_obj['value'] = max_hp
    return comp


def component_collision_box(
        width: float,
        height: float) -> Component:
    """
    Creates a collision box component.\n
    This sets the entity's collision box. It is necessary for most mobs.

    Parameters
    ----------
    width : float
        The width of the collision box. This is for both horizontal axes.
    height : float
        The height of the collision box.

    Returns
    -------
    Component
        A collision_box Component.
    """
    comp = Component('collision_box')
    comp.json_obj['width'] = width
    comp.json_obj['height'] = height
    return comp


def component_follow_range(rng: float) -> Component:
    """
    Creates a follow_range component.\n
    This component sets how far away the entity will pursue its target.

    Parameters
    ----------
    rng : float
        The maximum range at which the entity will pursue its target.

    Returns
    -------
    Component
        A follow_range Component.
    """
    comp = Component('follow_range')
    comp.json_obj['value'] = rng
    comp.json_obj['max'] = rng
    return comp


def component_no_dmg() -> Component:
    """
    Creates a damage_sensor component with all damage disabled.
    Note that an entity with this component can killed with the /kill command.

    Returns
    -------
    Component
        A damage_sensor Component which blocks all damage.
    """
    comp = Component('damage_sensor')
    comp.json_obj['triggers'] = {
        'on_damage': {
            'filters': {}
        },
        'deals_damage': False
    }
    return comp


def component_nav_generic(
        can_path_over_water: bool = True,
        avoid_water: bool = True,
        can_pass_doors: bool = True,
        can_open_doors: bool = False,
        avoid_damage_blocks: bool = True) -> Component:
    """
    Creates a navigation.generic component.\n
    This component allows the entity to pathfind walking, swimming, flying,
    jumping, and/or climbing paths. Various parameters determine what it can
    and can't do.

    Parameters
    ----------
    can_path_over_water : bool
        If true, the entity can generate paths over the surface of water.
    avoid_water : bool
        If true, the entity will avoid water.
    can_pass_doors : bool
        If true, the entity can generate paths which go through doors.
    can_open_doors : bool
        If true, the entity can generate paths which go through closed doors.
    avoid_damage_blocks : bool
        If true, the entity will avoid blocks which cause damage.

    Returns
    -------
    Component
        A navigation.generic Component.
    """
    comp = Component('navigation.generic')
    comp.json_obj['can_path_over_water'] = can_path_over_water
    comp.json_obj['avoid_water'] = avoid_water
    comp.json_obj['can_pass_doors'] = can_pass_doors
    comp.json_obj['can_open_doors'] = can_open_doors
    comp.json_obj['avoid_damage_blocks'] = avoid_damage_blocks
    return comp


def component_rideable(
        seat_positions: list[list[float]],
        family_types: list[str],
        pull_in_entities: bool = False) -> Component:
    """
    Creates a rideable component.\n
    This component allows other entities to ride on this one, with uses ranging
    from creating mounts like horses to being able to attach invisible utility
    entities.

    Parameters
    ----------
    seat_positions : list[list[float]]
        The set of seats on this entity. Each seat is defined by its position
        within the entity, relative to the entity's "feet".
        seat_positions is a list of three-float lists,
        representing coordinates.
        For example: [[0.0, 0.0, 0.0], [0.0, 0.5, 1.0]]
    family_types : list[str]
        The entity families which are allowed to ride this entity.
    pull_in_entities : bool
        If true, this entity will cause valid riders to enter an open seat
        if they touch.

    Returns
    -------
    Component
        A ridable Component.
    """
    # seat_positions error checks
    if type(seat_positions) is not list:
        raise TypeError(
            f"seat_positions is type {type(seat_positions)} instead of a list"
        )
    for pos_set in seat_positions:
        if type(pos_set) is not list:
            raise TypeError(
                f"An element of seat_positions is type {type(pos_set)} "
                "instead of a list"
            )
        if len(pos_set) != 3:
            raise ValueError(
                f"An element of seat_positions has {len(pos_set)} elements "
                "but it must have exactly 3"
            )
        for coord in pos_set:
            if type(coord) is not float and type(coord) is not int:
                raise TypeError(
                    f"An element in a seat position is type {type(coord)} "
                    "instead of a number"
                )
    # family_types error checks
    if type(family_types) is not list:
        raise TypeError(
            f"family_types is type {type(family_types)} instead of a list"
        )
    for family in family_types:
        if type(family) is not str:
            raise TypeError(
                f"An element of family_types is type {type(family)} "
                "instead of a string"
            )
    # pull_in_entities error check
    if type(pull_in_entities) is not bool:
        raise TypeError(
            f"pull_in_entities is type {type(pull_in_entities)} "
            "instead of a bool"
        )
    # Component assembly
    comp = Component('rideable')
    comp.json_obj['seat_count'] = len(seat_positions)
    comp.json_obj['family_types'] = family_types
    comp.json_obj['pull_in_entities'] = pull_in_entities
    seat_list = []
    for s in seat_positions:
        seat_list.append({
            'position': s
        })
    comp.json_obj['seats'] = seat_list
    return comp


def component_list_pathfinding(
        target_family: str,
        reached_event: str,
        sensor_range: float = 3) -> list[Component]:
    """
    Creates a set of Components which together make an entity walk
    towards a designated point.\n
    The target point must an entity with family target_family.\n

    Parameters
    ----------
    target_family : str
        The family ID of the pathfinding target. It's generally a good idea to
        make this unique for each pathfinding target so there's no possibility
        of the pathfinder getting confused.
    reached_event : str
        The event which will be called in the pathfinder upon reaching
        the target.
    sensor_range : float
        The maximum distance from the pathfinding target at which reached_event
        will be called.

    Returns
    -------
    list[Component]
        The Components returned are behavior.nearest_attackable_target,
        behavior.melee_attack, entity_sensor, and attack.
    """
    nat = Component('behavior.nearest_attackable_target')
    nat.json_obj = {
        "priority": 0,
        "reselect_targets": True,
        "target_search_height": 1000,
        "within_radius": 1000,
        "scan_interval": 20,
        "must_see": False,
        "entity_types": [
            {
                "filters": {
                    "test": "is_family",
                    "subject": "other",
                    "value": target_family
                },
                "max_dist": 1000
            }
        ]
    }
    att = component_attack(0)
    # ranged = Component('behavior.ranged_attack')
    # ranged.json_obj = {
    #     "priority": 0,
    #     "attack_radius": 1.0
    # }
    ranged = Component('behavior.melee_attack')
    ranged.json_obj = {
        "priority": 0,
        "reach_multiplier": 0.0
    }
    sensor = Component('entity_sensor')
    sensor.json_obj = {
        "event_filters": [
            {
                "test": "is_family",
                "subject": "other",
                "value": target_family
            }
        ],
        "event": reached_event,
        "sensor_range": sensor_range
    }
    return [
        nat,
        att,
        ranged,
        sensor
    ]


def component_no_knockback() -> Component:
    """
    Creates a knockback_resistance component with maximum resistance.

    Returns
    -------
    Component
        A knockback_resistance Component with maximum value.
    """
    comp = Component('knockback_resistance')
    comp.json_obj = {
        "value": 1.0
    }
    return comp


def component_shooter(
        projectile: str,
        potion_effect: int = None) -> Component:
    """
    Creates a shooter component.\n
    This component determines what kind of projectile an entity can shoot,
    as well as some other settings. Making an entity shoot requires the
    additional use of behavior.ranged_attack and at least one targeting
    component.

    Parameters
    ----------
    projectile : str
        The entity ID of the projectile to be used.
    potion_effect : int
        Numerical ID of a potion effect the projectile will apply on hit.

    Returns
    -------
    Component
        A shooter Component.
    """
    comp = Component('shooter')
    comp.json_obj = {
        "def": projectile
    }
    if potion_effect is not None:
        comp.json_obj['aux_val'] = potion_effect
    return comp


def tag_sensor(
        tag: str,
        event: str) -> Component:
    """
    Creates an environment_sensor component which waits for the entity to
    gain a specific tag, and then calls an event.\n
    For a sensor which can detect a variety of tags, use tag_sensor_list().

    Parameters
    ----------
    tag : str
        The tag which, when applied to this entity, will trigger the event.
    event : str
        The event which will be called.

    Returns
    -------
    Component
        An environment_sensor Component which detects a specific tag being
        applied to the entity.
    """
    comp = Component('environment_sensor')
    comp.json_obj = {
        "triggers": [
            {
                "filters": {
                    "test": "has_tag",
                    "value": tag
                },
                "event": event
            }
        ]
    }
    return comp


def tag_sensor_list(
        tags: list[str],
        events: list[str]) -> Component:
    """
    Creates an environment_sensor component which waits for the entity to
    gain any of a set of tags, and then calls the corresponding event.

    Parameters
    ----------
    tags : list[str]
        A list of tags which, when applied to this entity, will trigger the
        event name in at the same position in the events parameter.
    events : list[str]
        The list of events which will be called when the tag in the
        corresponding position of the tags list is added to the entity.

    Returns
    -------
    Component
        An environment_sensor Component which detects when any of a set of tags
        are applied to the entity and calls a corresponding event.
    """
    # Error checks
    for tag in tags:
        if type(tag) is not str:
            raise TypeError(
                f"An element of tags is type {type(tag)} "
                "instead of a string"
            )
    for event in events:
        if type(event) is not str:
            raise TypeError(
                f"An element of events is type {type(event)} "
                "instead of a string"
            )
    # Component construction
    comp = Component('environment_sensor')
    comp.json_obj = {
        "triggers": []
    }
    for n in range(0, len(tags)):
        obj = {
            "filters": {
                "test": "has_tag",
                "value": tags[n]
            },
            "event": events[n]
        }
        comp.json_obj['triggers'].append(obj)
    return comp
