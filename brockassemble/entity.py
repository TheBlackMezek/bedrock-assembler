"""
Module containing classes which abstract elements of entity JSON,
as well as a few functions for generating basic entities.
"""
import json
from brockassemble.component import (
    Component,
    component_skin_id,
    component_attack,
    component_health,
    component_timer,
    component_movement,
    component_no_dmg,
    component_scale,
    component_collision_box
)
import copy


RP_ENTITY_FORMAT_VERSION = '1.8.0'
BP_ENTITY_FORMAT_VERSION = '1.16.0'
BANCO_FORMAT_VERSION = '1.10.0'
ENTITY_GRAPHICS_FORMAT_VERSION = '1.10.0'


def basic_rp_entity(id: str, namespace: str) -> dict:
    """
    Creates a barebones JSON dict for an invisible entity resource file.

    Parameters
    ----------
    id : str
        Unique identifier for this entity. Should be lower case.
    namespace : str
        Grouping prefix for this entity. Should be lower case. Can be any
        text you like, but use of the name of the team which is making the
        map or addon is recommended.

    Returns
    -------
    dict
        The JSON (stored as a dict) for a barebones client entity file. It will
        not render in the game, and it will use a black and magenta spawn egg
        (missing texture colors) to indicate that no entity-specific colors
        have been set for it.
    """
    entity = {}
    entity['format_version'] = RP_ENTITY_FORMAT_VERSION
    desc = {}
    desc['identifier'] = namespace + ':' + id
    # This geometry is mostly arbitrary, it just needs to be something
    # guaranteed to exist.
    desc['geometry'] = {'default': 'geometry.humanoid.customSlim'}
    desc['spawn_egg'] = {'base_color': '#000000', 'overlay_color': '#ff00ff'}
    entity['minecraft:client_entity'] = {}
    entity['minecraft:client_entity']['description'] = desc
    return entity


def basic_bp_entity(id: str, namespace: str) -> dict:
    """
    Creates a barebones JSON dict for an entity behavior file.

    Parameters
    ----------
    id : str
        Unique identifier for this entity. Should be lower case.
    namespace : str
        Grouping prefix for this entity. Should be lower case. Can be any
        text you like, but use of the name of the team which is making the
        map or addon is recommended.

    Returns
    -------
    dict
        The JSON (stored as a dict) for a barebones server entity file. It will
        be summonable with commands and have a spawn egg. It will not be able
        to use experimental components. Empty dicts for entity components,
        component groups, and events are added for convenience.
    """
    entity = {}
    entity['format_version'] = BP_ENTITY_FORMAT_VERSION

    desc = {}
    desc['identifier'] = namespace + ':' + id
    desc['is_spawnable'] = True
    desc['is_summonable'] = True
    desc['is_experimental'] = False

    comp = {}
    comp_g = {}
    events = {}

    entity['minecraft:entity'] = {}
    entity['minecraft:entity']['description'] = desc
    entity['minecraft:entity']['components'] = comp
    entity['minecraft:entity']['component_groups'] = comp_g
    entity['minecraft:entity']['events'] = events
    return entity


def _replace_list_string_variables(
        lst: list,
        string_variables: dict
    ) -> None:
    """
    Loops through all dict values and list elements in lst and replace every 
    substring which matches a string_variables key prepended with % with the 
    corresponding string_variables value.

    For example, {'name': 'Foo'} would replace every substring '%name' in 
    every string dict value and list element with 'Foo'.

    If string_variables value is not a string, can also replace an exact match 
    with the value.

    For example, {'damage': 5} would replace '%damage' with 5, but 
    'My damage is %damage' will produce an error.

    Parameters
    ----------
    list : list
        The list to recursively loop through. Only str values will be modified.
    string_variables : dict
        The string variable patterns to match and replace. See above for
        instructions.
    
    Returns
    -------
    None
        Changes to lst are done in-place.
    """
    for i in range(0,len(lst)):
        for s in string_variables:
            var_str = '%'+s
            if lst[i] == var_str:
                lst[i] = string_variables[s]
            elif type(lst[i]) == str and var_str in lst[i]:
                lst[i] = lst[i].replace(var_str, string_variables[s])
        if type(lst[i]) == dict:
            replace_obj_string_variables(lst[i], string_variables)
        if type(lst[i]) == list:
            _replace_list_string_variables(lst[i], string_variables)


def replace_obj_string_variables(
        obj: dict,
        string_variables: dict) -> None:
    """
    Loop through all dict values and list elements in obj and replace every 
    substring which matches a string_variables key prepended with % with the 
    corresponding string_variables value.

    For example, {'name': 'Foo'} would replace every substring '%name' in 
    every string dict value and list element with 'Foo'.

    If string_variables value is not a string, can also replace an exact match 
    with the value.

    For example, {'damage': 5} would replace '%damage' with 5, but 
    'My damage is %damage' will produce an error.

    Parameters
    ----------
    obj : dict
        The dict to recursively loop through. Only str values will be modified.
    string_variables : dict
        The string variable patterns to match and replace. See above for
        instructions.
    
    Returns
    -------
    None
        Changes to obj are done in-place.
    """
    for i in obj:
        for s in string_variables:
            var_str = '%'+s
            if obj[i] == var_str:
                obj[i] = string_variables[s]
            elif type(obj[i]) == str and var_str in obj[i]:
                obj[i] = obj[i].replace(var_str, string_variables[s])
        if type(obj[i]) == dict:
            replace_obj_string_variables(obj[i], string_variables)
        if type(obj[i]) == list:
            _replace_list_string_variables(obj[i], string_variables)


class AnimTimelineItem:
    """
    Class which represents one point on an animation timeline.

    Attributes
    ----------
    trigger_time : float
    commands : list[str]
    """
    def __init__(
            self,
            trigger_time: float = None,
            commands: list[str] = []):
        self.trigger_time: float = trigger_time
        """The time in seconds when this timeline item will trigger."""
        self.commands: list[str] = commands
        """
        A list of commands which will be run at this point in the timeline.
        Note that this only works for behavior pack animations.
        """

    def add_command(self, cmd: str) -> None:
        """
        Adds a command which will be run when this timeline item is triggered.

        Parameters
        ----------
        cmd : str
            The command which will be run.
        """
        self.commands.append(cmd)

    def add_commands(self, cmds: list[str]) -> None:
        """
        Adds a list of commands which will be run when this timeline 
        item is triggered.

        Parameters
        ----------
        cmds : list[str]
            The commands which will be run.
        """
        self.commands.extend(cmds)

    def get_json(self) -> list[str] | str:
        """
        Compile this timeline item's attributes into
        data ready for writing into an animation's JSON file.

        Returns
        -------
        list[str] | str
            Returns a string if there is only one command.
            Otherwise, returns the list of all commands.
        """
        if len(self.commands) == 1:
            return self.commands[0]
        else:
            return self.commands


class Animation:
    """
    Class which represents an animation.
    Note that this represents a single animation, and must be added to an
    AnimationFile object for writing to file.

    Attributes
    ----------
    identifier : str
    looping : bool
    length : float
    timeline_items : list[AnimTimelineItem]
    """
    def __init__(
            self,
            identifier: str,
            looping: bool = False,
            length: float = None,
            timeline_items: list = None):
        self.identifier: str = identifier
        """The unique ID for this animation."""
        self.looping: bool = looping
        """Whether this animation should loop when it finishes."""
        self.length: float = length
        """Duration of this animation in seconds."""
        self.timeline_items: list[AnimTimelineItem]
        """All of the timeline items, or keyframes, in this animation."""
        if timeline_items is None:
            self.timeline_items = []
        else:
            self.timeline_items = timeline_items

    def add_timeline_item(self, item: AnimTimelineItem) -> None:
        """
        Adds a timeline item to this animation.

        Parameters
        ----------
        item : AnimTimelineItem
            The timeline item to be added.
        """
        self.timeline_items.append(item)

    def add_timeline_items(self, items: list[AnimTimelineItem]) -> None:
        """
        Adds a list of timeline items to this animation.

        Parameters
        ----------
        items : list[AnimTimelineItem]
            The list of timeline items to be added.
        """
        self.timeline_items.extend(items)

    def get_json(self) -> dict:
        """
        Compile this animation into a dict ready for writing into a JSON file.

        Returns
        -------
        dict
            A JSON-ready object representing this animation.
        """
        obj = {}

        if self.looping:
            obj['loop'] = self.looping
        if self.length is not None:
            obj['animation_length'] = self.length
        if len(self.timeline_items) > 0:
            timeline = {}
            for item in self.timeline_items:
                timeline[str(item.trigger_time)] = item.get_json()
            obj['timeline'] = timeline

        return obj


class AnimationFile:
    """
    Class which represents a set of animations in a file.

    Attributes
    ----------
    format_version : str
    animations: list[Animation]
    """
    def __init__(self, animations: list[Animation] = []):
        self.format_version: str = "1.8.0"
        """The format version for Bedrock to use when reading this file."""
        self.animations: list[Animation] = animations
        """The list of animations contained in this file."""

    def add_anim(self, anim: Animation) -> None:
        """
        Adds an animation to this file.

        Parameters
        ----------
        anim : Animation
            The animation to be added.
        """
        self.animations.append(anim)

    def add_anims(self, anims: list[Animation]) -> None:
        """
        Adds a list of animations to this file.

        Parameters
        ----------
        anims : list[Animation]
            The list of animations to be added.
        """
        self.animations.extend(anims)

    def get_json(self) -> dict:
        """
        Compile this object into a dict ready for writing as a JSON animation file.

        Returns
        -------
        dict
            A JSON-ready object representing this set of animations.
        """
        obj = {}

        obj['format_version'] = self.format_version
        obj['animations'] = {}
        for anim in self.animations:
            obj['animations'][anim.identifier] = anim.get_json()

        return obj


class AncoState:
    """
    Class which represents an animation controller state.

    Attributes
    ----------
    identifier : str
    """
    def __init__(
            self,
            identifier: str,
            entry_commands: list[str]=None,
            exit_commands: list[str]=None,
            transitions: list[list[str]]=None,
            animations: list[str]=None,
            transition_time: float=None):
        self.identifier = identifier
        """ID of the anco state, must be unique within the anco."""
        self._transitions = []
        """
        A list of two-element lists, where subelement 1 is the state to
        transition to, and subelement 2 is the condition.

        Example: [
            ['init', 'query.all_animations_finished'],
            ['dead', 'query.health <= 0']
        ]
        """
        self._on_entry = []
        """
        A list of commands to execute when the state is entered.\n
        Each command must include a forward slash / prefix.
        """
        self._on_exit = []
        """
        A list of commands to execute when the state is exited.\n
        Each command must include a forward slash / prefix.
        """
        self._animations = []
        """A list of animations to play while in this state."""
        self._transition_time = transition_time
        """
        Time in seconds during which animations from this state will blend
        with animations in the next state.
        """

        if entry_commands is not None:
            self._on_entry = entry_commands
        if exit_commands is not None:
            self._on_exit = exit_commands
        if transitions is not None:
            self.add_transitions(transitions)
        if animations is not None:
            self._animations = animations

    def get_json(self) -> dict:
        """
        Builds a JSON-ready dict of this anco state which can be used in an 
        animation controller.

        Returns
        -------
        dict
            A JSON-ready object representing this animation controller state.
        """
        obj = {}

        if len(self._transitions) > 0:
            transitions = []
            for i in self._transitions:
                transitions.append({ i[0]:i[1] })
            obj['transitions'] = transitions

        if len(self._on_entry) > 0:
            obj['on_entry'] = self._on_entry

        if len(self._on_exit) > 0:
            obj['on_exit'] = self._on_exit

        if len(self._animations) > 0:
            obj['animations'] = self._animations

        if self._transition_time is not None:
            obj['blend_transition'] = self._transition_time

        return obj

    def add_entry_commands(self, cmd_list: list[str]) -> None:
        """
        Adds a list of commands to execute when the state is entered.\n

        Parameters
        ----------
        cmd_list : list[str]
            The list of commands to execute.
            Each command must include a forward slash / prefix.
        """
        for i in cmd_list:
            self._on_entry.append(i)

    def add_entry_command(self, cmd: str) -> None:
        """
        Adds a command to execute when the state is entered.\n

        Parameters
        ----------
        cmd : str
            The command to execute.
            The command must include a forward slash / prefix.
        """
        self._on_entry.append(cmd)

    def add_exit_commands(self, cmd_list: list[str]) -> None:
        """
        Adds a list of commands to execute when the state is exited.\n

        Parameters
        ----------
        cmd_list : list[str]
            The list of commands to execute.
            Each command must include a forward slash / prefix.
        """
        for i in cmd_list:
            self._on_exit.append(i)

    def add_exit_command(self, cmd: str) -> None:
        """
        Adds a command to execute when the state is exited.\n

        Parameters
        ----------
        cmd : str
            The command to execute.
            The command must include a forward slash / prefix.
        """
        self._on_exit.append(cmd)

    def add_animations(self, anim_list: list[str]) -> None:
        """
        Adds a list of animations to play while in this state.

        Parameters
        ----------
        anim_list : list[str]
            The list the IDs of animation to play.
        """
        for i in anim_list:
            self._animations.append(i)

    def add_animation(self, anim: str) -> None:
        """
        Adds an animation to play while in this state

        Parameters
        ----------
        anim : str
            The ID of the animation to play.
        """
        self._animations.append(anim)

    def add_transitions(self, lst: list[list[str]]):
        """
        Adds a list of transitions from this state to others.

        Parameters
        ----------
        lst : list[list[str]]
            lst is a list of 2-element lists. 
            lst[n][0] = state_id, lst[n][1] = condition_string\n
            Example: [
                ['init', 'query.all_animations_finished'],\n
                ['dead', 'query.health <= 0']
            ]
        """
        for i in lst:
            self._transitions.append([i[0], i[1]])

    def add_transition(self, state_id: str, condition_string: str) -> None:
        """
        Adds a transition into another state.

        Parameters
        ----------
        state_id : str
            The state to transition into.
        condition_string : str
            The condition under which to make the transition.
        """
        self._transitions.append([state_id, condition_string])


class EventRandomizer:
    """
    Class which stores data and generates a JSON dict for an
    event randomization option
    """
    def __init__(self,
                 weight: int = 1,
                 add_groups: list = None,
                 remove_groups: list = None,
                 set_properties: dict = None):
        """
        Each key of set_properties is an entity property ID, and each 
        value is what that property will be set to.
        """
        self._weight = weight
        """The weight of this randomizer option against others in the event"""
        self._add_groups = add_groups
        """Component group IDs to add if this randomization option is chosen"""
        self._remove_groups = remove_groups
        """
        Component group IDs to remove if this randomization option 
        is chosen
        """
        self._set_properties = set_properties
        """
        Dict of entity properties to set if this randomization option is 
        chosen. Each key is an entity property ID, and each value is what that 
        property will be set to.
        """

    def get_json(self):
        """
        Builds a JSON-ready dict of this event which can be used in a 
        Bedrock behavior pack event
        """
        obj = {}
        obj['weight'] = self._weight
        if self._add_groups is not None:
            obj['add'] = {}
            obj['add']['component_groups'] = self._add_groups
        if self._remove_groups is not None:
            obj['remove'] = {}
            obj['remove']['component_groups'] = self._remove_groups
        if self._set_properties is not None:
            obj['set_property'] = self._set_properties
        return obj


class Event:
    """Class which stores data and generates a JSON dict for an event"""
    def __init__(self,
                 identifier: str,
                 namespace: str=None,
                 add_groups: list[str]=None,
                 remove_groups: list[str]=None,
                 randomizers: list[EventRandomizer]=None,
                 sequential_events: list['Event']=None,
                 set_properties: list[list] = None):
        """Format for set_properties is a list of lists,\n
        [prop_id: str, value: any, optional no_quotes: bool]"""
        self.identifier = identifier
        """Name of the event"""
        self.namespace = namespace
        """Namespace of the event"""
        self._add_groups = []
        """IDs of component groups this event will add"""
        self._remove_groups = []
        """IDs of component groups this event will remove"""
        self._randomizers = []
        """List of EventRandomizers in this event"""
        self._sequential_events = []
        """List of sub-Events which are sequentially executed in this event"""
        self._set_properties = {}
        """
        A dict of entity property alterations. Takes the form of:\n
        key = entity property ID\n
        value = what to set the entity property to
        """
        self._next_event = None
        """ID of an event which will be called after this one"""

        if add_groups is not None:
            self.add_add_groups(add_groups)
        if remove_groups is not None:
            self.add_remove_groups(remove_groups)
        if randomizers is not None:
            self.add_randomizers(randomizers)
        if sequential_events is not None:
            self.add_sequential_events(sequential_events)
        if set_properties is not None:
            for s in set_properties:
                self.add_set_property(*s)

    def add_add_group(self, group: str) -> None:
        """Adds a component group ID to be added when this event is called"""
        self._add_groups.append(group)

    def add_add_groups(self, groups: list[str]) -> None:
        """Adds a list of component group IDs to be added when 
        this event is called"""
        for i in groups:
            self._add_groups.append(i)

    def add_remove_group(self, group: str) -> None:
        """Adds a component group ID to be removed when this event is called"""
        self._remove_groups.append(group)

    def add_remove_groups(self, groups: list[str]) -> None:
        """
        Adds a list of component group IDs to be removed when 
        this event is called
        """
        for i in groups:
            self._remove_groups.append(i)

    def add_randomizer(self, r: EventRandomizer) -> None:
        """Adds an EventRandomizer to this event"""
        self._randomizers.append(r)

    def add_randomizers(self, r: list[EventRandomizer]) -> None:
        """Adds a list of EventRandomizers to this event"""
        for i in r:
            self._randomizers.append(i)

    def add_sequential_event(self, r: 'Event') -> None:
        """
        Appends a sub-Event to a list of sub-Events which will be
        executed in sequence within this Event
        """
        self._sequential_events.append(r)

    def add_sequential_events(self, r: list['Event']) -> None:
        """
        Appends a list of sub-Events to a list of sub-Events which will be 
        executed in sequence within this Event
        """
        for i in r:
            self._sequential_events.append(i)

    def add_set_property(
            self,
            prop_id: str,
            value,
            no_quotes: bool = False) -> None:
        """
        Adds an entity property change to this Event\n
        if no_quotes is false, string values will be surrounded by single
        quotes, e.g. \'new value\'
        """
        if type(value) is str and not no_quotes:
            value = f"'{value}'"
        self._set_properties['property:'+prop_id] = value

    def get_id(self) -> str:
        """Returns the event identifier with a namespace if it has one"""
        if self.namespace is not None:
            return self.namespace + ':' + self.identifier
        else:
            return self.identifier

    def get_json(self) -> dict:
        """
        Builds a JSON-ready dict of this event which can be used in a 
        Bedrock behavior pack behavior file
        """
        obj = {}
        # Randomizers need to be nested in a sequence
        if len(self._randomizers) > 0:
            obj['sequence'] = []
            if len(self._add_groups) > 0:
                sub_obj = {}
                sub_obj['add'] = {}
                sub_obj['add']['component_groups'] = self._add_groups
                obj['sequence'].append(sub_obj)
            if len(self._remove_groups) > 0:
                sub_obj = {}
                sub_obj['remove'] = {}
                sub_obj['remove']['component_groups'] = self._remove_groups
                obj['sequence'].append(sub_obj)
            if len(self._set_properties) > 0:
                set_obj = {}
                for key in self._set_properties.keys():
                    set_obj[key] = self._set_properties[key]
                sub_obj = {'set_property': set_obj}
                obj['sequence'].append(sub_obj)
            rand_obj = {}
            rand_obj['randomize'] = []
            for i in self._randomizers:
                rand_obj['randomize'].append(i.get_json())
            obj['sequence'].append(rand_obj)
        # Normal no-randomizer event creation
        else:
            if len(self._add_groups) > 0:
                obj['add'] = {}
                obj['add']['component_groups'] = self._add_groups
            if len(self._remove_groups) > 0:
                obj['remove'] = {}
                obj['remove']['component_groups'] = self._remove_groups
            if len(self._set_properties) > 0:
                set_obj = {}
                for key in self._set_properties.keys():
                    set_obj[key] = self._set_properties[key]
                obj['set_property'] = set_obj
        # If there are sequential events, make the primary event the first part
        # in a sequence
        if len(self._sequential_events) > 0:
            sequence = [copy.deepcopy(obj)]
            for e in self._sequential_events:
                sequence.append(e.get_json())
            obj = {"sequence": sequence}
        # Call a successive event if there is one
        if self._next_event is not None:
            obj['trigger'] = {
                "event": self._next_event,
                "target": "self"
            }
        return obj


class ComponentGroup:
    """
    Class which stores data and generates a JSON dict for a component group
    """
    def __init__(
            self,
            identifier: str,
            namespace: str=None,
            skin_id: int=None,
            timer_len: float=None,
            timer_event: str=None,
            hp: int=None,
            attack: int=None,
            move_speed: float=None,
            has_physics: bool=False,
            no_damage: bool=False,
            scale: float=None):
        self.identifier = identifier
        """Name of the component group"""
        self._namespace = namespace
        """Namespace of the component group"""
        self._components = []
        """List of Component objects which comprise this component group"""

        if skin_id is not None:
            self.add_component(component_skin_id(skin_id))

        if timer_len is not None and timer_event is not None:
            self.add_component(component_timer(timer_len, timer_event))
        elif timer_len is not None:
            print(
                f'ERROR: Component group {self.get_id()}: '
                'Timer length given without event'
            )
        elif timer_event is not None:
            print(
                f'ERROR: Component group {self.get_id()}: '
                'Timer event given without length'
            )

        if hp is not None:
            self.add_component(component_health(hp))
        if attack is not None:
            self.add_component(component_attack(attack))
        if move_speed is not None:
            self.add_component(component_movement(move_speed))
        if has_physics:
            self.add_component(Component('physics'))
        if no_damage:
            self.add_component(component_no_dmg())
        if scale is not None:
            self.add_component(component_scale(scale))

    def add_component(self, comp: Component) -> None:
        """Adds a Component to this component group"""
        self._components.append(comp)

    def add_component_list(self, comp_list: list[Component]) -> None:
        """Adds a list of Components to this component group"""
        for c in comp_list:
            self.add_component(c)

    def get_id(self) -> str:
        """
        Returns the component group identifier with a namespace if it has one
        """
        if self._namespace is not None:
            return self._namespace + ':' + self.identifier
        else:
            return self.identifier

    def get_json(self) -> dict:
        """
        Builds a JSON-ready dict of this component group which can be used 
        in a Bedrock behavior pack behavior file
        """
        obj = {}
        for c in self._components:
            obj[c.get_id()] = c.json_obj
        return obj


class EntityProperty:
    """
    Base class which stores data and generates a JSON dict for an entity 
    property\n
    Intended as a parent class, not for direct use
    """
    def __init__(self,
                 identifier: str,
                 default, # intentionally not hinted, can be a variety of types
                 client_sync: bool = False) -> None:
        self.identifier: str = identifier
        """Name of this entity property"""
        self._values = None
        """Possible values"""
        self._default = default
        """Default value"""
        self._client_sync: bool = client_sync
        """Should this entity property be synced to clientside?"""
        self._data_type: str = None
        """Data type name"""

    def get_json(self) -> dict:
        """Builds a JSON-ready dict of this entity property which can be used 
        in a Bedrock behavior pack behavior file"""
        ret = {
            "values": self._values
        }
        ret['default'] = self._default
        ret['type'] = self._data_type
        if self._client_sync is not False:
            ret['client_sync'] = self._client_sync
        return ret


class PropertyRange(EntityProperty):
    """
    Class which stores data and generates a JSON dict for an entity 
    property with a range of possible integer values
    """
    def __init__(self,
                 identifier: str,
                 min: int,
                 max: int,
                 default: int,
                 client_sync: bool = False) -> None:
        super().__init__(identifier, default, client_sync)
        self._values = {
            "min": min,
            "max": max
        }
        """Possible values"""
        self._data_type = 'int'

    def get_json(self) -> dict:
        ret = {
            "range": [self._values['min'], self._values['max']]
        }
        ret['default'] = self._default
        ret['type'] = self._data_type
        if self._client_sync is not False:
            ret['client_sync'] = self._client_sync
        return ret


class PropertyBool(EntityProperty):
    """
    Class which stores data and generates a JSON dict for an entity 
    property with possible values of True and False
    """
    def __init__(self,
                 identifier: str,
                 default: bool,
                 client_sync: bool = False) -> None:
        super().__init__(identifier, default, client_sync)
        self._values = [
            False,
            True
        ]
        'Possible values'
        self._data_type = 'bool'


class PropertyEnum(EntityProperty):
    """
    Class which stores data and generates a JSON dict for an entity 
    property with an arbitrary set of individual possible values
    """
    def __init__(self,
                 identifier: str,
                 values: list,
                 default, # intentionally not hinted, can be a variety of types
                 client_sync: bool = False) -> None:
        super().__init__(identifier, default, client_sync)
        self._values = values
        """Possible values"""
        self._data_type = 'enum'


class Behaviors:
    """
    Class which stores data and generates a JSON dict for an entity's 
    behavior file
    """
    def __init__(
            self,
            identifier: str,
            string_variables: dict=None,
            runtime_identifier: str=None):
        self.identifier = identifier
        """ID of the entity, including namespace"""
        self.is_spawnable = True
        """Should this entity have a spawn egg?"""
        self.is_summonable = True
        """Should this entity be summonable with commands?"""
        self.is_experimental = False
        """Uncertain of usage, might enable experimental components"""
        self._bancos = []
        """The list of animation controller IDs which this entity uses"""
        self._animations = []
        """The list of behavior pack animation IDs which this entity uses"""
        self.components = []
        """The list of groupless Components in this entity"""
        self.component_groups = []
        """The list of ComponentGroups in this entity"""
        self.events = []
        """List of Events in this entity"""
        self.spawn_groups = []
        """List of component group IDs added to the entity on spawn"""
        self.spawn_randomizers = []
        """List of EventRandomizers to be used in the spawn event"""
        self.spawn_sequential_events = []
        """List of sub-Events to be used in the spawn event"""
        self.properties = []
        """List of EntityProperties in this entity"""
        self.spawn_properties = {}
        """Dict of entity properties to set when the entity spawns.\n
        Each key is the ID of an entity property, 
        and each value is what the property will be set to,"""
        self._lstate_names = {}
        """
        Dict to facilitate connection of nonlinear loop states.\n
        Each key is an arbitrary name given to an lstate.\n
        Each value is a list of strings. Element 0 is always the true 
        identifier for the named lstate. The rest of the elements are the IDs 
        of states which connect to it.
        """
        self.string_variables = string_variables
        """A dict of string key-value pairs """
        self.runtime_identifier = runtime_identifier
        """Vanilla entity ID to inherit from"""

    def get_json(self) -> dict:
        """
        Builds a JSON-ready dict of these entity behaviors which can be 
        written as a Bedrock behavior pack behavior file
        """
        # Create vanilla spawn event
        if (
            len(self.spawn_groups) > 0 or
            len(self.spawn_randomizers) > 0 or
            len(self.spawn_sequential_events) > 0 or
            len(self.spawn_properties) > 0
        ):
            spawn_event = self.get_event('minecraft:entity_spawned')
            if spawn_event is None:
                spawn_event = Event('entity_spawned', namespace='minecraft')
                self.events.append(spawn_event)
            spawn_event.add_add_groups(self.spawn_groups)
            spawn_event.add_randomizers(self.spawn_randomizers)
            spawn_event.add_sequential_events(self.spawn_sequential_events)
            spawn_event._set_properties = self.spawn_properties

        # Remove component groups from branching connections
        if len(self._lstate_names) > 0:
            for k, v in self._lstate_names.items():
                event = self.get_event(v[0])
                if event is not None:
                    for i in range(1, len(v)):
                        if v[i] not in event._remove_groups:
                            event.add_remove_group(v[i])

        # Make basic bvr desc section and basic structure
        obj = {}
        obj['format_version'] = BP_ENTITY_FORMAT_VERSION
        entity_obj = {}
        obj['minecraft:entity'] = entity_obj
        desc = {}
        desc['identifier'] = self.identifier
        if self.runtime_identifier is not None:
            desc['runtime_identifier'] = self.runtime_identifier
        desc['is_spawnable'] = self.is_spawnable
        desc['is_summonable'] = self.is_summonable
        desc['is_experimental'] = self.is_experimental
        anim_dict = {}
        if len(self._bancos) > 0:
            desc['scripts'] = { 'animate': [] }
            for n in range(0,len(self._bancos)):
                desc['scripts']['animate'].append({f'banco_{n}':'1'})
                anim_dict[f'banco_{n}'] = self._bancos[n]
        if len(self._animations) > 0:
            for anim in self._animations:
                anim_dict[anim.identifier] = anim.identifier
        if len(anim_dict) > 0:
            desc['animations'] = anim_dict
        if len(self.properties) > 0:
            prop_obj = {}
            for prop in self.properties:
                prop_obj['property:'+prop.identifier] = prop.get_json()
            desc['properties'] = prop_obj
        entity_obj['description'] = desc

        # Make main bvr sections
        components = {}
        for c in self.components:
            components['minecraft:' + c.comp_type] = c.json_obj
        entity_obj['components'] = components

        if len(self.component_groups) > 0:
            component_groups = {}
            for g in self.component_groups:
                component_groups[g.get_id()] = g.get_json()
            entity_obj['component_groups'] = component_groups

        if len(self.events) > 0:
            events = {}
            for e in self.events:
                events[e.get_id()] = e.get_json()
            entity_obj['events'] = events

        # Resolve branching lstate names
        if len(self._lstate_names) > 0:
            s = json.dumps(obj)
            for k, v in self._lstate_names.items():
                if v[0] is not None:
                    s = s.replace(k, v[0])
            obj = json.loads(s)

        # Resolve string variables
        if self.string_variables is not None:
            replace_obj_string_variables(obj, self.string_variables)

        # Behavior creation complete
        return obj

    def add_banco(self, banco: str) -> None:
        """Add a behavior pack animation controller ID"""
        self._bancos.append(banco)

    def add_animation(self, animation: Animation) -> None:
        """Add a behavior pack animation"""
        self._animations.append(animation)

    def get_event(self, event_id) -> Event:
        """Returns an Event if one of event_id ID is found, otherwise None"""
        for i in self.events:
            if i.get_id() == event_id:
                return i
        return None

    def add_property(self, prop: EntityProperty) -> None:
        """Add an EntityProperty"""
        self.properties.append(prop)

    def get_component(self, component_id) -> Component:
        """
        Returns a Component if one of component_id ID is found, 
        otherwise None
        """
        for i in self.components:
            if i.comp_type == component_id:
                return i
        return None


class AnimationController:

    def __init__(self, identifier, initial_state='init', string_variables=None):
        self.identifier = identifier
        self.states = []
        self.string_variables = string_variables
        if initial_state is not None:
            self.initial_state = initial_state
    
    def get_json(self):
        obj = {}
        obj['format_version'] = BANCO_FORMAT_VERSION
        banco = {}
        banco['initial_state'] = self.initial_state
        banco_states = {}

        for i in self.states:
            banco_states[i.identifier] = i.get_json()
            
        banco['states'] = banco_states
        obj['animation_controllers'] = {}
        obj['animation_controllers'][self.identifier] = banco

        if self.string_variables is not None:
            replace_obj_string_variables(obj, self.string_variables)

        return obj

    def add_state(self, state):
        self.states.append(state)
    
    def add_states(self, states: list) -> None:
        for s in states:
            self.add_state(s)
    
    def has_state(self, state_name):
        for i in self.states:
            if i.identifier == state_name:
                return True
        return False
     
    def get_state(self, state_name):
        for i in self.states:
            if i.identifier == state_name:
                return i
        return None


class EntityGraphics:
    def __init__(
            self,
            identifier,
            string_variables=None,
            material='basic',
            render_controller='controller.render.default_controller',
            egg_color_1='#550077',
            egg_color_2='#88cc88',
            texture_path=None,
            invisible=False,
            geo=None,
            animations=None,
            animate_list=None,
            particle_dict=None):
        """
        texture_path automatically adds 'textures/entity/' to the start\n
        geo automatically adds 'geometry.' to the start\n
        If texture_path or geo are not provided, identifier will be used as:\n
        textures/entity/identifier\n
        geometry.identifier\n
        texture_path and geo can also be dicts, and prefixes will be applied to each element
        """
        self.identifier = identifier
        self.material = material
        self.render_controller = render_controller
        self.egg_color_1 = egg_color_1
        self.egg_color_2 = egg_color_2
        self.anim_obj = animations
        self.animate_list = animate_list
        self.particle_obj = None
        self.init_list = None
        self.pre_anim = None
        self.invisible = invisible
        self.string_variables = string_variables
        self.scale = 1.0
        self.particle_obj = particle_dict

        if texture_path is None:
            self.texture_path = 'textures/entity/' + self.identifier
        elif type(texture_path) is str:
            self.texture_path = 'textures/entity/' + texture_path
        elif type(texture_path) is dict:
            self.texture_path = texture_path
            for key in self.geo.keys():
                self.texture_path[key] = 'textures/entity/' + self.texture_path[key]

        if geo is None:
            self.geo = 'geometry.' + self.identifier
        elif type(geo) is str:
            self.geo = 'geometry.' + geo
        elif type(geo) is dict:
            self.geo = geo
            for key in self.geo.keys():
                self.geo[key] = 'geometry.' + self.geo[key]

    def add_animations(self, anim_obj: dict):
        if self.anim_obj is None:
            self.anim_obj = anim_obj
        else:
            self.anim_obj.update(anim_obj)
    
    def add_particles(self, obj: dict):
        if self.particle_obj is None:
            self.particle_obj = obj
        else:
            self.particle_obj.update(obj)

    def add_animate_list(self, animate_list: list):
        if self.animate_list is None:
            self.animate_list = animate_list
        else:
            self.animate_list.extend(animate_list)

    def add_script_initialize(self, init_list: list):
        if self.init_list is None:
            self.init_list = init_list
        else:
            self.init_list.extend(init_list)

    def add_script_pre_anim(self, pre_anim: list):
        if self.pre_anim is None:
            self.pre_anim = pre_anim
        else:
            self.pre_anim.extend(pre_anim)

    def add_ranco(self, ranco: AnimationController):
        self.add_animations({ranco.identifier: ranco.identifier})
        self.add_animate_list([ranco.identifier])

    def add_humanoid_animations(self):
        self.add_animations({
            "root": "controller.animation.humanoid.root",
            "base_controller": "controller.animation.player.base",
            "hudplayer":  "controller.animation.humanoid.hudplayer",
            "humanoid_base_pose": "animation.humanoid.base_pose",
            "look_at_target": "controller.animation.humanoid.look_at_target",
            "look_at_target_ui": "animation.player.look_at_target.ui",
            "look_at_target_default": "animation.humanoid.look_at_target.default",
            "look_at_target_gliding": "animation.humanoid.look_at_target.gliding",
            "look_at_target_swimming": "animation.humanoid.look_at_target.swimming",
            "look_at_target_inverted": "animation.player.look_at_target.inverted",
            "cape": "animation.player.cape",
            "move.arms": "animation.player.move.arms",
            "move.legs": "animation.player.move.legs",
            "swimming": "animation.player.swim",
            "swimming.legs": "animation.player.swim.legs",
            "riding.arms": "animation.player.riding.arms",
            "riding.legs": "animation.player.riding.legs",
            "holding": "animation.player.holding",
            "brandish_spear": "animation.humanoid.brandish_spear",
            "charging": "animation.humanoid.charging",
            "attack.positions": "animation.player.attack.positions",
            "attack.rotations": "animation.player.attack.rotations",
            "sneaking": "animation.player.sneaking",
            "bob": "animation.player.bob",
            "damage_nearby_mobs": "animation.humanoid.damage_nearby_mobs",
            "fishing_rod": "animation.humanoid.fishing_rod",
            "use_item_progress": "animation.humanoid.use_item_progress",
            "skeleton_attack": "animation.skeleton.attack",
            "sleeping": "animation.player.sleeping",
            "first_person_base_pose": "animation.player.first_person.base_pose",
            "first_person_empty_hand": "animation.player.first_person.empty_hand",
            "first_person_swap_item": "animation.player.first_person.swap_item",
            "first_person_attack_controller": "controller.animation.player.first_person_attack",
            "first_person_attack_rotation": "animation.player.first_person.attack_rotation",
            "first_person_attack_rotation_item": "animation.player.first_person.attack_rotation",
            "first_person_vr_attack_rotation": "animation.player.first_person.vr_attack_rotation",
            "first_person_walk": "animation.player.first_person.walk",
            "first_person_map_controller": "controller.animation.player.first_person_map",
            "first_person_map_hold": "animation.player.first_person.map_hold",
            "first_person_map_hold_attack": "animation.player.first_person.map_hold_attack",
            "first_person_map_hold_off_hand": "animation.player.first_person.map_hold_off_hand",
            "first_person_map_hold_main_hand": "animation.player.first_person.map_hold_main_hand",
            "first_person_crossbow_equipped": "animation.player.first_person.crossbow_equipped",
            "third_person_crossbow_equipped": "animation.player.crossbow_equipped",
            "third_person_bow_equipped": "animation.player.bow_equipped",
            "crossbow_hold": "animation.player.crossbow_hold",
            "crossbow_controller": "controller.animation.player.crossbow",
            "shield_block_main_hand": "animation.player.shield_block_main_hand",
            "shield_block_off_hand": "animation.player.shield_block_off_hand",
            "blink": "controller.animation.persona.blink"
        })
        self.add_animate_list(['root'])
        self.add_script_initialize([
            "variable.is_holding_right = 0.0;",
            "variable.is_blinking = 0.0;",
            "variable.last_blink_time = 0.0;",
            "variable.hand_bob = 0.0;",
            "variable.is_paperdoll = 0.0;",
            "variable.is_first_person = 0.0;",
            "variable.map_face_icon = 0.0;",
            "variable.item_use_normalized = 0.0;"
        ])
        self.add_script_pre_anim([
            "variable.helmet_layer_visible = 1.0;",
            "variable.leg_layer_visible = 1.0;",
            "variable.boot_layer_visible = 1.0;",
            "variable.chest_layer_visible = 1.0;",
            "variable.attack_body_rot_y = Math.sin(360*Math.sqrt(variable.attack_time)) * 5.0;",
            "variable.tcos0 = (math.cos(query.modified_distance_moved * 38.17) * query.modified_move_speed / variable.gliding_speed_value) * 57.3;"
        ])

    def get_json(self):
        obj = {}
        obj['format_version'] = ENTITY_GRAPHICS_FORMAT_VERSION

        desc = {}
        desc['identifier'] = self.identifier
        if not self.invisible:
            desc['materials'] = {'default':self.material}
            desc['render_controllers'] = [self.render_controller]

            if type(self.geo) is str:
                desc['geometry'] = {'default':self.geo}
            elif type(self.geo) is dict:
                desc['geometry'] = self.geo

            if type(self.texture_path) is str:
                desc['textures'] = {'default':self.texture_path}
            elif type(self.texture_path) is dict:
                desc['textures'] = self.texture_path

        else:
            desc['geometry'] = {'default':'geometry.humanoid'}

        desc['spawn_egg'] = {'base_color':self.egg_color_1,'overlay_color':self.egg_color_2}
        
        if self.anim_obj is not None:
            desc['animations'] = self.anim_obj
        
        if self.particle_obj is not None:
            desc['particle_effects'] = self.particle_obj

        script_obj = {'scale':str(self.scale)}
        if self.animate_list is not None:
            script_obj['animate'] = self.animate_list
        if self.init_list is not None:
            script_obj['initialize'] = self.init_list
        if self.pre_anim is not None:
            script_obj['pre_animation'] = self.pre_anim
        desc['scripts'] = script_obj

        obj['minecraft:client_entity'] = {'description':desc}

        if self.string_variables is not None:
            replace_obj_string_variables(obj, self.string_variables)

        return obj


class Entity:
    def __init__(
            self,
            namespace,
            name,
            string_variables=None,
            id=None,
            egg_name=None,
            collision_x=0,
            collision_y=0,
            hp=None,
            attack=None,
            move_speed=None,
            has_physics=True,
            no_damage=False,
            spawn_groups=None,
            has_graphics=False,
            entity_graphics=None,
            invisible=False,
            runtime_identifier=None,
            despawnable=False,
            ambient_sound=None,
            hurt_sound=None,
            death_sound=None,
            step_sound=None,
            sounds_pitch_range=[0.8, 1.2],
            sounds_volume=1.0):
        self.namespace = namespace
        self.name = name
        self.bancos = []
        self.current_state=0
        self.rancos = []

        self.ambient_sound=ambient_sound
        self.hurt_sound=hurt_sound
        self.death_sound=death_sound
        self.step_sound=step_sound
        self.sounds_pitch_range=sounds_pitch_range
        self.sounds_volume=sounds_volume

        if id is not None:
            self.identifier = id
        else:
            self.identifier = name.lower().replace(' ', '_')
        
        if egg_name is not None:
            self.egg_name = egg_name
        else:
            self.egg_name = 'Spawn ' + name

        self.string_variables = string_variables

        if entity_graphics is not None:
            self.graphics = entity_graphics
        elif has_graphics:
            self.graphics = EntityGraphics(self.get_id(), string_variables=self.string_variables, invisible=invisible)
        else:
            self.graphics = None

        self.behaviors = Behaviors(self.get_id(), self.string_variables, runtime_identifier)
        self.add_component(component_collision_box(collision_x, collision_y))
        if hp is not None:
            self.add_component(component_health(hp))
        if attack is not None:
            self.add_component(component_attack(attack))
        if move_speed is not None:
            self.add_component(component_movement(move_speed))
        if has_physics:
            self.add_component(Component('physics'))
        if no_damage:
            self.add_component(component_no_dmg())
        if spawn_groups is not None:
            self.add_spawn_groups(spawn_groups)
        if despawnable:
            despawn_group = ComponentGroup('despawn')
            despawn_group.add_component(Component('instant_despawn'))
            self.add_component_group(despawn_group)
            self.add_event(Event('despawn', add_groups=['despawn']))

    def get_id(self):
        return self.namespace + ':' + self.identifier

    def add_component(self, component):
        self.behaviors.components.append(component)

    def add_component_list(self, comp_list):
        for c in comp_list:
            self.add_component(c)

    def add_component_group(self, group):
        self.behaviors.component_groups.append(group)

    def add_event(self, event):
        self.behaviors.events.append(event)

    def create_banco(self, banco_name, initial_state=None):
        banco = AnimationController('controller.animation.' + self.identifier + '_' + banco_name,
                                    initial_state=initial_state,
                                    string_variables=self.string_variables)
        self.bancos.append(banco)

        if self.behaviors is not None:
            self.behaviors.add_banco(banco.identifier)
        else:
            print('WARNING: banco added to entity without behaviors')

        return len(self.bancos)-1

    def add_banco(self, banco):
        self.bancos.append(banco)
        if self.behaviors is not None:
            self.behaviors.add_banco(banco.identifier)
        else:
            print('WARNING: banco added to entity without behaviors')
        return len(self.bancos)-1

    def create_ranco(self, ranco_name, initial_state=None):
        ranco = AnimationController('controller.animation.' + self.identifier + '_' + ranco_name,
                                    initial_state=initial_state,
                                    string_variables=self.string_variables)
        self.rancos.append(ranco)

        if self.graphics is not None:
            self.graphics.add_ranco(ranco)
        else:
            print('WARNING: ranco added to entity without graphics')

        return len(self.rancos)-1

    def add_ranco(self, ranco):
        self.rancos.append(ranco)
        if self.graphics is not None:
            self.graphics.add_ranco(ranco)
        else:
            print('WARNING: ranco added to entity without graphics')
        return len(self.rancos)-1

    def add_banco_state(self, banco_idx, state):
        self.bancos[banco_idx].add_state(state)

    def add_ranco_state(self, ranco_idx, state):
        self.rancos[ranco_idx].add_state(state)

    def add_spawn_group(self, group):
        self.behaviors.spawn_groups.append(group)

    def add_spawn_groups(self, groups):
        for i in groups:
            self.behaviors.spawn_groups.append(i)

    def set_identifier(self, id):
        self.identifier = id
        self.behaviors.identifier = self.get_id()

    def current_lstate(self):
        return 'state_' + str(self.current_state)

    def next_lstate(self):
        return 'state_' + str(self.current_state+1)

    def prev_lstate(self):
        return 'state_' + str(self.current_state-1)

    def add_loop_state(
            self,
            banco_id=0,
            ranco_id=0,
            components=None,
            entry_commands=None,
            exit_commands=None,
            timer_len=None,
            last_state=False,
            name=None,
            connection_list=None,
            timer_state=None,
            hp=None,
            attack=None,
            move_speed=None,
            no_damage=False,
            animation=None,
            end_anim_with_state=True,
            anim_blend_time=0.2,
            set_properties: dict=None):
        group = ComponentGroup(self.current_lstate(), skin_id=self.current_state)
        if timer_len is not None:
            if timer_state is not None:
                group.add_component(component_timer(timer_len, timer_state))
                if connection_list is None:
                    connection_list = [timer_state]
                else:
                    connection_list.append(timer_state)
            elif not last_state:
                group.add_component(component_timer(timer_len, self.next_lstate()))
            else:
                group.add_component(component_timer(timer_len, 'state_0'))
        if hp is not None:
            group.add_component(component_health(hp))
        if attack is not None:
            group.add_component(component_attack(attack))
        if move_speed is not None:
            group.add_component(component_movement(move_speed))
        if no_damage:
            group.add_component(component_no_dmg()) 
        if components is not None:
            group.add_component_list(components)
        self.add_component_group(group)

        if entry_commands is not None or exit_commands is not None:
            banco_state = AncoState(self.current_lstate())
            banco_state.add_transition('init', 'query.skin_id!='+str(self.current_state))
            if entry_commands is not None:
                for i in entry_commands:
                    banco_state.add_entry_command(i)
            if exit_commands is not None:
                for i in exit_commands:
                    banco_state.add_exit_command(i)
            self.add_banco_state(banco_id, banco_state)

            self.bancos[banco_id].initial_state = 'init'
            if not self.bancos[banco_id].has_state('init'):
                self.add_banco_state(banco_id, AncoState('init'))
            self.bancos[banco_id].get_state('init').add_transition(self.current_lstate(), 'query.skin_id=='+str(self.current_state))

        if animation is not None:
            ranco_state = AncoState(self.current_lstate())
            if end_anim_with_state:
                ranco_state.add_transition('init', 'query.skin_id!='+str(self.current_state))
            else:
                ranco_state.add_transition('init', 'query.all_animations_finished')
            ranco_state.add_animation(animation)
            ranco_state._transition_time=anim_blend_time
            self.add_ranco_state(ranco_id, ranco_state)

            self.rancos[ranco_id].initial_state = 'init'
            if not self.rancos[ranco_id].has_state('init'):
                self.add_ranco_state(ranco_id, AncoState('init'))
            self.rancos[ranco_id].get_state('init').add_transition(self.current_lstate(), 'query.skin_id=='+str(self.current_state))

        if self.current_state == 0 and set_properties is not None:
            self.behaviors.spawn_properties.update(set_properties)

        event = Event(
            self.current_lstate(),
            add_groups=[self.current_lstate()],
            remove_groups=[self.prev_lstate()]
        )
        if set_properties is not None:
            event._set_properties = set_properties
        self.add_event(event)
        if last_state:
            for i in self.behaviors.events:
                if i.identifier == 'state_0':
                    i.remove_groups = [self.current_lstate()]

        if name is not None:
            if name in self.behaviors._lstate_names:
                self.behaviors._lstate_names[name][0] = self.current_lstate()
            else:
                self.behaviors._lstate_names[name] = [self.current_lstate()]

        if connection_list is not None:
            for i in connection_list:
                if i not in self.behaviors._lstate_names:
                    self.behaviors._lstate_names[i] = [None]
                self.behaviors._lstate_names[i].append(self.current_lstate())

        self.current_state += 1

    def get_sounds_obj(self):
        obj = {}

        events = {}
        if self.ambient_sound is not None:
            events['ambient'] = self.ambient_sound
        if self.step_sound is not None:
            events['step'] = self.step_sound
        if self.hurt_sound is not None:
            events['hurt'] = self.hurt_sound
        if self.death_sound is not None:
            events['death'] = self.death_sound
        if len(events) > 0:
            obj['events'] = events

        obj['pitch'] = self.sounds_pitch_range
        obj['volume'] = self.sounds_volume

        return obj


def build_projectile(
        id,
        entity_graphics,
        damage,
        namespace='%namespace',
        string_variables=None,
        name=None,
        collision_box_size=0.25,
        knockback=True,
        enflame=False,
        spawn_entity=None,
        spawn_chance=100.0,
        spawn_count=1,
        hit_sound='bow.hit',
        stick_in_ground=False,
        destroyed_on_hit=True,
        spread=10,
        power=1.0,
        gravity=0.05,
        remove_on_hit: bool = False) -> Entity:
    """
    If used, spawn_entity must be the ID of a mob
    (minus namespace, e.g. chicken instead of minecraft:chicken)
    """
    if name is None:
        name = id
    entity = Entity(
        namespace,
        name,
        string_variables,
        id,
        collision_x=collision_box_size,
        collision_y=collision_box_size,
        entity_graphics=entity_graphics,
        runtime_identifier='minecraft:arrow',
        despawnable=True
    )
    #entity = Entity('%namespace', name, string_variables, id, collision_x=collision_box_size, collision_y=collision_box_size, entity_graphics=entity_graphics)
    projectile_component = Component('projectile')
    projectile_json_obj = {
        "on_hit": {
            "impact_damage": {
                "damage": damage,
                "knockback": knockback,
                "semi_random_diff_damage": False,
                "destroy_on_hit": destroyed_on_hit
            },
        },
        #"multiple_targets": not destroyed_on_hit,
        "hit_sound": hit_sound,
        "power": power,
        "gravity": gravity,
        "uncertainty_base": spread,
        "uncertainty_multiplier": 0,
        "anchor": 1,
        "should_bounce": True,
        #"stop_on_hurt": {},
        "offset": [0,-0.1,0],
        "catch_fire": enflame
    }

    if stick_in_ground:
        projectile_json_obj['on_hit']['stick_in_ground'] = {"shake_time":0.35}
    if spawn_entity is not None:
        projectile_json_obj['on_hit']['spawn_chance'] = {
            "spawn_definition": spawn_entity,
            "first_spawn_percent_chance": spawn_chance,
            "first_spawn_count": spawn_count
        }
    if destroyed_on_hit:
        projectile_json_obj['stop_on_hurt'] = {}
    if remove_on_hit:
        projectile_json_obj['on_hit']['remove_on_hit'] = {}
    #     projectile_json_obj['on_hit']['remove_on_hit'] = {}

    projectile_component.json_obj = projectile_json_obj
    entity.add_component(projectile_component)

    optimizer_component = Component('conditional_bandwidth_optimization')
    optimizer_json_obj = {
        "default_values": {
          "max_optimized_distance": 80.0,
          "max_dropped_ticks": 10,
          "use_motion_prediction_hints": True
        }
    }

    #entity.add_component(optimizer_component)

    return entity
