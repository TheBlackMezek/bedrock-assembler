"""
Module containing the Component class and functions for generating various
entity components.
"""
from typing import Union


class Component:
    '''Base class for any addon file which uses a component system\n
    This includes entity behavior files and particles'''
    comp_type = 'UNDEFINED_COMPONENT_TYPE'
    json_obj = {}

    def __init__(self, type: str, priority: int = None):
        self.json_obj = {}
        self.comp_type = type
        if priority is not None:
            self.json_obj['priority'] = priority

    def get_id(self) -> str:
        "This entity's type prefixed with the 'minecraft:' namespace"
        return 'minecraft:' + self.comp_type


def component_family(families: list) -> Component:
    '''Creates a type_family component\n
    families must be a list of strings'''
    comp = Component('type_family')
    comp.json_obj['family'] = families
    return comp


def component_timer(length: float, event: str) -> Component:
    '''Creates a timer component\n
    Keep in mind you can only have one active at a time in an entity'''
    comp = Component('timer')
    comp.json_obj['randomInterval'] = False
    comp.json_obj['time'] = length
    comp.json_obj['time_down_event'] = {'event': event}
    return comp


def component_skin_id(skin_id: int) -> Component:
    '''Creates a skin_id component\n
    Useful for sending data between entity files, 
    but consider using entity properties instead'''
    comp = Component('skin_id')
    comp.json_obj['value'] = skin_id
    return comp


def component_variant(variant: int) -> Component:
    '''Creates a variant component\n
    Useful for sending data between entity files, 
    but consider using entity properties instead'''
    comp = Component('variant')
    comp.json_obj['value'] = variant
    return comp


def component_mark_variant(mark_variant: int) -> Component:
    '''Creates a mark_variant component\n
    Useful for sending data between entity files, 
    but consider using entity properties instead'''
    comp = Component('mark_variant')
    comp.json_obj['value'] = mark_variant
    return comp


def component_scale(scale: float) -> Component:
    '''Creates a scale component\n
    Changes the entity's visual size and hitbox'''
    comp = Component('scale')
    comp.json_obj['value'] = scale
    return comp


def component_movement(speed: float) -> Component:
    '''Creates a movement component\n
    This sets an entity's walkspeed, which can be further modified under 
    certain conditions by other components.'''
    comp = Component('movement')
    comp.json_obj['value'] = speed
    return comp


def component_stroll(
        speed: float = 1,
        priority: int = 5
    ) -> Component:
    '''Creates a behavior.random_stroll component\n
    Causes the entity to wander around randomly'''
    comp = Component('behavior.random_stroll', priority=priority)
    comp.json_obj['speed_multiplier'] = speed
    return comp


def component_random_look(priority: int=8) -> Component:
    '''Creates a behavior.random_look_around component\n
    Causes the entity to periodically rotate its head and body 
    in a random direction'''
    return(Component('behavior.random_look_around', priority=priority))


def component_attack(
        dmg: Union[int, list[int]],
        effect_id: str = None,
        effect_duration: float = None
    ) -> Component:
    '''Creates an attack \n
    Sets the properties of an entity's melee attack. 
    Does not set targeting or movement to make attacks actually happen.\n
    If dmg is a list, it must be 2 elements, a minimum and maximum.\n
    effect_id is the name of a potion effect to apply on hit.\n
    effect_duration is the time in seconds that potion effect will last.'''
    comp = Component('attack')
    comp.json_obj['damage'] = dmg
    if effect_id is not None:
        comp.json_obj['effect_name'] = effect_id
    if effect_duration is not None:
        comp.json_obj['effect_duration'] = effect_duration
    return comp


def component_melee_attack(
        speed_multiplier: float = None,
        track_target: bool = None,
        reach_multiplier: float = None
    ) -> Component:
    '''Creates a behavior.melee_attack component\n
    speed_multiplier is applied to the entity's movement \n
    track_target allows the entity to track its target even if 
    it doesn't have sensing. If not supplied, Bedrock defaults it to False.\n
    reach_multiplier uses the base size of the entity, which I think means 
    hitbox. If not supplied, Bedrock defaults it to 2.0.'''
    comp = Component('behavior.melee_attack')
    if speed_multiplier is not None:
        comp.json_obj['speed_multiplier'] = speed_multiplier
    if track_target is not None:
        comp.json_obj['track_target'] = track_target
    if reach_multiplier is not None:
        comp.json_obj['reach_multiplier'] = reach_multiplier
    return comp


def component_ranged_attack(
        attack_range: int = 15.0,
        interval_min: int = 1.0,
        interval_max: int = 3.0
    ) -> Component:
    '''Creates a behavior.ranged_attack component'''
    comp = Component('behavior.ranged_attack')
    comp.json_obj = {
        "attack_radius": attack_range,
        "attack_interval_min": interval_min,
        "attack_interval_max": interval_max
    }
    return comp


def component_area_attack(
        damage_range: float,
        dmg: int) -> Component:
    '''Creates an area_attack component\n
    This deals damage to every entity which comes within range'''
    comp = Component('area_attack')
    comp.json_obj['damage_range'] = damage_range
    comp.json_obj['damage_per_tick'] = dmg
    return comp


def component_health(max_hp: int):
    'Creates a health component'
    comp = Component('health')
    comp.json_obj['max'] = max_hp
    comp.json_obj['value'] = max_hp
    return comp


def component_collision_box(
        width: float,
        height: float) -> Component:
    'Creates a collision box component'
    comp = Component('collision_box')
    comp.json_obj['width'] = width
    comp.json_obj['height'] = height
    return comp


def component_follow_range(rng: float) -> Component:
    'Creates a follow_range component'
    comp = Component('follow_range')
    comp.json_obj['value'] = rng
    comp.json_obj['max'] = rng
    return comp


def component_no_dmg() -> Component:
    'Creates a damage_sensor component with all damage disabled'
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
    'Creates a navigation.generic component'
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
        pull_in_entities=False) -> Component:
    '''Creates a rideable component\n
    seat_positions is a list of three-float lists, for example: 
    [[0.0, 0.0, 0.0], [0.0, 0.5, 1.0]]'''
    comp = Component('rideable')
    comp.json_obj['seat_count'] = len(seat_positions)
    comp.json_obj['family_types'] = family_types
    comp.json_obj['pull_in_entities'] = pull_in_entities
    seat_list = []
    for s in seat_positions:
        seat_list.append({
            'position':s
        })
    comp.json_obj['seats'] = seat_list
    return comp


def component_list_pathfinding(
        target_family: str,
        reached_event: str,
        sensor_range: float=3) -> list:
    '''Returns a set of components which together make an entity walk 
    towards a designated point\n
    The target point must an entity with family target_family\n
    reached_event is the event which will be called upon reaching the target\n
    sensor_range is how far away the entity can be to 
    call reached_event\n
    The components returned are behavior.nearest_attackable_target, 
    behavior.melee_attack, entity_sensor, and attack'''
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
    #ranged = Component('behavior.ranged_attack')
    #ranged.json_obj = {
    #    "priority": 0,
    #    "attack_radius": 1.0
    #}
    ranged = Component('behavior.melee_attack')
    ranged.json_obj = {
        "priority": 0,
        "reach_multiplier": 0.0
    }
    sensor = Component('entity_sensor')
    sensor.json_obj = {
        "event_filters": [
            {
                "test":"is_family",
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
    'Creates a knockback_resistance component with maximum resistance'
    comp = Component('knockback_resistance')
    comp.json_obj = {
        "value": 1.0
    }
    return comp


def component_shooter(
        projectile: str,
        potion_effect: int = -1) -> Component:
    '''Creates a shooter component\n
    projectile is an entity ID\n
    potion_effect is a vanilla ID number'''
    comp = Component('shooter')
    comp.json_obj = {
        "def": projectile
    }
    if potion_effect != -1:
        comp.json_obj['aux_val'] = potion_effect
    return comp


def tag_sensor(
        tag: str,
        event: str) -> Component:
    '''Creates an environment_sensor component which waits for the entity to 
    gain the tag passed in, and then calls event'''
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
    '''Creates an environment_sensor component which waits for the entity to 
    gain any of the tags passed in, and then calls the corresponding event'''
    comp = Component('environment_sensor')
    comp.json_obj = {
        "triggers": []
    }
    for n in range(0,len(tags)):
        obj = {
            "filters": {
                "test": "has_tag",
                "value": tags[n]
            },
            "event": events[n]
        }
        comp.json_obj['triggers'].append(obj)
    return comp

