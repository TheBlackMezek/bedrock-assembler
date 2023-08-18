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
from typing import Any


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
        string_variables: dict) -> None:
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
    for i in range(0, len(lst)):
        for s in string_variables:
            var_str = '%'+s
            if lst[i] == var_str:
                lst[i] = string_variables[s]
            elif type(lst[i]) is str and var_str in lst[i]:
                lst[i] = lst[i].replace(var_str, string_variables[s])
        if type(lst[i]) is dict:
            replace_obj_string_variables(lst[i], string_variables)
        if type(lst[i]) is list:
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
            elif type(obj[i]) is str and var_str in obj[i]:
                obj[i] = obj[i].replace(var_str, string_variables[s])
        if type(obj[i]) is dict:
            replace_obj_string_variables(obj[i], string_variables)
        if type(obj[i]) is list:
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
        """
        Parameters
        ----------
        trigger_time : float
            The time in seconds when this timeline item will trigger.
        commands : list[str]
            A list of commands which will be run at this point in the timeline.
            Note that this only works for behavior pack animations.
        """

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
            timeline_items: list[AnimTimelineItem] = None):
        """
        Parameters
        ----------
        identifier : str
            The unique ID for this animation.
        looping : bool
            Whether this animation should loop when it finishes.
        length : float
            Duration of this animation in seconds.
        timeline_items : list[AnimTimelineItem]
            All of the timeline items, or keyframes, in this animation.
        """

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
        """
        Parameters
        ----------
        animations : list[Animation]
            The list of animations contained in this file.
        """

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
        Compile this object into a dict ready for writing
        as a JSON animation file.

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
            entry_commands: list[str] = None,
            exit_commands: list[str] = None,
            transitions: list[list[str]] = None,
            animations: list[str] = None,
            transition_time: float = None):
        """
        Parameters
        ----------
        identifier : str
            ID of the anco state, must be unique within the anco.
        entry_commands : list[str]
            A list of commands to execute when the state is entered.\n
            Each command must include a forward slash / prefix.
        exit_commands : list[str]
            A list of commands to execute when the state is exited.\n
            Each command must include a forward slash / prefix.
        transitions : list[list[str]]
            A list of two-element lists, where subelement 1 is the state to
            transition to, and subelement 2 is the condition.\n
            Example: [
                ['init', 'query.all_animations_finished'],
                ['dead', 'query.health <= 0']
            ]
        animations: list[str]
            A list of animations to play while in this state.
        transition_time : float
            Time in seconds during which animations from this state will blend
            with animations in the next state.
        """

        self.identifier = identifier
        """ID of the anco state, must be unique within the anco."""
        self._transitions: list[list[str]] = []
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
                transitions.append({i[0]: i[1]})
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
        Adds an animation to play while in this state.

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
    Class which represents an event randomization option.
    """
    def __init__(
            self,
            weight: int = 1,
            add_groups: list[str] = None,
            remove_groups: list[str] = None,
            set_properties: dict = None):
        """
        Parameters
        ----------
        weight : int
            The weight of this randomizer option against others in the event.
            This is best thought of like entering a number of tickets into a
            raffle. If randomizer A has weight 1 and randomizer B has weight 1,
            there's a 50/50 chance of picking either. But if B has weight 2,
            there is now a 33/66 chance.
        add_groups : list[str]
            Component group IDs to add if
            this randomization option is chosen.
        remove_groups : list[str]
            Component group IDs to remove if
            this randomization option is chosen.
        set_properties : dict
            Dict of entity properties to set if this randomization option is
            chosen. Each key is an entity property ID, and each value is what
            that property will be set to.
        """
        self._weight = weight
        """
        The weight of this randomizer option against others in the event.
        This is best thought of like entering a number of tickets into a
        raffle. If randomizer A has weight 1 and randomizer B has weight 1,
        there's a 50/50 chance of picking either. But if B has weight 2,
        there is now a 33/66 chance.
        """
        self._add_groups = add_groups
        """
        Component group IDs to add if this randomization option is chosen.
        """
        self._remove_groups = remove_groups
        """
        Component group IDs to remove if
        this randomization option is chosen.
        """
        self._set_properties = set_properties
        """
        Dict of entity properties to set if this randomization option is
        chosen. Each key is an entity property ID, and each value is what that
        property will be set to.
        """

    def get_json(self) -> dict:
        """
        Builds a JSON-ready dict of this randomizer option which can be used in
        an event.

        Returns
        -------
        dict
            A JSON-ready object representing this event randomizer option.
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
    """
    Class which represents an event.

    Attributes
    ----------
    identifier : str
    namespace : str
    """
    def __init__(
            self,
            identifier: str,
            namespace: str = None,
            add_groups: list[str] = None,
            remove_groups: list[str] = None,
            randomizers: list[EventRandomizer] = None,
            sequential_events: list['Event'] = None,
            set_properties: list[list] = None,
            next_event: str = None):
        """
        Parameters
        ----------
        identifier : str
            The ID for this event. Must be unique within the behavior file.
        namespace : str
            The namespace for this event. Not required for custom events, but
            hard-coded Bedrock events require the "minecraft" namespace.
        add_groups : list[str]
            IDs of component groups this event will add.
        remove_groups : list[str]
            IDs of component groups this event will remove.
        randomizers : list[EventRandomizer]
            List of EventRandomizers in this event. When the event is called,
            one of these will be randomly selected, in addition to the normal
            add and remove groups.
        sequential_events : list[Event]
            List of sub-Events which are sequentially executed by this event.
        set_properties : list
            Entity property values to set when this event is called.
            Format for set_properties is a list of lists, where each sub-list
            has this format:\n
            [prop_id: str, value: any, optional no_quotes: bool]\n
            By default, entity property values are treated like a string and
            surrounded qith quotes. If no_quotes is used and set to True,
            string values will instead have no quotes.
        next_event : str
            ID of another event which will be called after this one.
        """

        self.identifier = identifier
        """The ID for this event. Must be unique within the behavior file."""
        self.namespace = namespace
        """
        The namespace for this event. Not required for custom events, but
        hard-coded Bedrock events require the "minecraft" namespace.
        """
        self._add_groups = []
        """IDs of component groups this event will add."""
        self._remove_groups = []
        """IDs of component groups this event will remove."""
        self._randomizers = []
        """
        List of EventRandomizers in this event. When the event is called,
        one of these will be randomly selected, in addition to the normal
        add and remove groups.
        """
        self._sequential_events = []
        """List of sub-Events which are sequentially executed in this event."""
        self._set_properties = {}
        """
        A dict of entity property alterations. Takes the form of:\n
        key = Entity property ID.\n
        value = What to set the entity property to.
        """
        self._next_event = None
        """ID of another event which will be called after this one."""

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
        """
        Sets another component group to be added when this event is called.

        Parameters
        ----------
        group : str
            The ID of the component group to be added.
        """
        self._add_groups.append(group)

    def add_add_groups(self, groups: list[str]) -> None:
        """
        Add a list of component groups to be added when this event is called.

        Parameters
        ----------
        groups : list[str]
            The IDs of the component groups to be added.
        """
        for i in groups:
            self._add_groups.append(i)

    def add_remove_group(self, group: str) -> None:
        """
        Sets another component group to be removed when this event is called.

        Parameters
        ----------
        group : str
            The ID of the component group to be removed.
        """
        self._remove_groups.append(group)

    def add_remove_groups(self, groups: list[str]) -> None:
        """
        Add a list of component groups to be removed when this event is called.

        Parameters
        ----------
        groups : list[str]
            The IDs of the component groups to be removed.
        """
        for i in groups:
            self._remove_groups.append(i)

    def add_randomizer(self, r: EventRandomizer) -> None:
        """
        Add a randomization option to this event, which will be added to the
        pool of other EventRandomizers to be selected from when this event is
        called.

        Parameters
        ----------
        r : EventRandomizer
            The EventRandomizer to be added.
        """
        self._randomizers.append(r)

    def add_randomizers(self, r: list[EventRandomizer]) -> None:
        """
        Add a list of randomization options to this event, which will be added
        to the pool of other EventRandomizers to be selected from when this
        event is called.

        Parameters
        ----------
        r : list[EventRandomizer]
            The EventRandomizers to be added.
        """
        for i in r:
            self._randomizers.append(i)

    def add_sequential_event(self, r: 'Event') -> None:
        """
        Appends a sub-Event to the list of sub-Events which will be
        executed in sequence when this Event is called.

        Parameters
        ----------
        r : Event
            The Event to be added.
        """
        self._sequential_events.append(r)

    def add_sequential_events(self, r: list['Event']) -> None:
        """
        Appends a list of sub-Events to the list of sub-Events which will be
        executed in sequence when this Event is called.

        Parameters
        ----------
        r : list[Event]
            The Events to be added.
        """
        for i in r:
            self._sequential_events.append(i)

    def add_set_property(
            self,
            prop_id: str,
            value,
            no_quotes: bool = False) -> None:
        """
        Make this event set an additional entity property value when it is
        called.

        Parameters
        ----------
        prop_id : str
            The ID of the entity property to be set.
        value : any
            The value which the entity property will be set to.
        no_quotes : bool
            Whether the value should be surrounded by quotes
            (treated like a string). If no_quotes is false, string values will
            be surrounded by single quotes, e.g. \'new value\'.
        """
        if type(value) is str and not no_quotes:
            value = f"'{value}'"
        self._set_properties['property:'+prop_id] = value

    def get_id(self) -> str:
        """
        Returns the event identifier, with a namespace if it has one.

        Returns
        -------
        str
            The full ID of this event.
        """
        if self.namespace is not None:
            return self.namespace + ':' + self.identifier
        else:
            return self.identifier

    def get_json(self) -> dict:
        """
        Builds a JSON-ready dict of this event which can be used in
        a behavior file.

        Returns
        -------
        dict
            A JSON-ready object representing this event.
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
    Class which represents a component group.

    Attributes
    ----------
    identifier : str
    """
    def __init__(
            self,
            identifier: str,
            namespace: str = None,
            skin_id: int = None,
            timer_len: float = None,
            timer_event: str = None,
            hp: int = None,
            attack: int = None,
            move_speed: float = None,
            has_physics: bool = False,
            no_damage: bool = False,
            scale: float = None):
        """
        Parameters
        ----------
        identifier : str
            The ID of this component group. Must be unique within the entity.
        namespace : str
            The namespace of this component group. Not required.
        skin_id : int
            If used, a skin_id Component will be added to this component group
            with the value of this parameter.
        timer_len : float
            If used with timer_event, a timer Component will be added to this
            component group with a duration of timer_len. Does nothing
            on its own.
        timer_event : str
            If used with timer_len, a timer Component will be adedd to this
            component group which calls an event with ID timer_event when it
            ends. Does nothing on its own.
        hp : int
            If used, a health Component will be added to this component group,
            setting the entity's maximum health hp the value of this parameter.
        attack : int
            If used, an attack Component will be added to this component group,
            setting the entity's melee damage to the value of this parameter.
        move_speed : float
            If used, a movement Component will be added to this component
            group, setting the entity's walkspeed to the value
            of this parameter.
        has_physics : bool
            If True, a physics Component will be added to this component group,
            making the entity affected by gravity and collisions, assuming it
            doesn't already have a physics component.
        no_damage : bool
            If true, a damage_sensor Component set to deny all damage will be
            added to this component group. The entity can still be killed with
            /kill.
        scale : float
            If used, a scale Component will be added to this component group,
            multiplying the visual and hitbox size of the entity by the value
            of this parameter.
        """

        self.identifier: str = identifier
        """The ID of this component group. Must be unique within the entity."""
        self._namespace: str = namespace
        """The namespace of this component group. Not required."""
        self._components: list[Component] = []
        """List of Component objects which comprise this component group."""

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
        """
        Adds a Component to this component group.

        Parameters
        ----------
        comp : Component
            The Component to be added.
        """
        self._components.append(comp)

    def add_component_list(self, comp_list: list[Component]) -> None:
        """
        Adds a list of Components to this component group.

        Parameters
        ----------
        comp : list[Component]
            The Components to be added.
        """
        for c in comp_list:
            self.add_component(c)

    def get_id(self) -> str:
        """
        Returns the component group identifier, with a namespace if it has one.

        Returns
        -------
        str
            The full ID of this component group.
        """
        if self._namespace is not None:
            return self._namespace + ':' + self.identifier
        else:
            return self.identifier

    def get_json(self) -> dict:
        """
        Builds a JSON-ready dict of this component group which can be used in
        a behavior file.

        Returns
        -------
        dict
            A JSON-ready object representing this component group.
        """
        obj = {}
        for c in self._components:
            obj[c.get_id()] = c.json_obj
        return obj


class EntityProperty:
    """
    Base class which represents an entity property.

    Intended as a parent class, not for direct use.

    Attributes
    ----------
    identifier : str
    """
    def __init__(
            self,
            identifier: str,
            default: Any,
            client_sync: bool = False):
        """
        Parameters
        ----------
        identifier : str
            The ID of this entity property. Must be unique within the entity.
        default : Any
            The default value of this entity property. Data type will depend
            on the type of entity property this is.
        client_sync : bool
            Whether this entity property should be synced clientside, or only
            tracked on the server.
        """

        self.identifier: str = identifier
        """The ID of this entity property. Must be unique within the entity."""
        self._values = None
        """This entity property's range of possible values."""
        self._default = default
        """The default value of this entity property."""
        self._client_sync: bool = client_sync
        """
        Whether this entity property should be synced clientside, or only
        tracked on the server.
        """
        self._data_type: str = None
        """The name of this entity property's data type."""

    def get_json(self) -> dict:
        """
        Builds a JSON-ready dict of this entity property which can be used in
        an entity behavior file.

        Returns
        -------
        dict
            A JSON-ready object representing this entity property.
        """
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
    Class which represents an entity property with a range of possible
    integer values.
    """
    def __init__(
            self,
            identifier: str,
            min: int,
            max: int,
            default: int,
            client_sync: bool = False):
        """
        Parameters
        ----------
        identifier : str
            The ID of this entity property. Must be unique within the entity.
        min : int
            The minimum possible value of this entity property.
        max : int
            The maximium possible value of this entity property.
        default : int
            The default value of this entity property.
        client_sync : bool
            Whether this entity property should be synced clientside, or only
            tracked on the server.
        """

        super().__init__(identifier, default, client_sync)
        self._values = {
            "min": min,
            "max": max
        }
        """
        This entity property's range of possible values.

        Values
        ------
        "min"
            The minimum possible value.
        "max"
            The maximum possible value.
        """
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
    Class which represents an entity property with possible values of
    True and False.
    """
    def __init__(
            self,
            identifier: str,
            default: bool,
            client_sync: bool = False):
        """
        Parameters
        ----------
        identifier : str
            The ID of this entity property. Must be unique within the entity.
        default : bool
            The default value of this entity property.
        client_sync : bool
            Whether this entity property should be synced clientside, or only
            tracked on the server.
        """

        super().__init__(identifier, default, client_sync)
        self._values = [
            False,
            True
        ]
        """
        This entity property's range of possible values. As a bool property,
        the only possible values are False and True.
        """
        self._data_type = 'bool'


class PropertyEnum(EntityProperty):
    """
    Class which represents an entity property with an arbitrary set of
    individual possible values.
    """
    def __init__(
            self,
            identifier: str,
            values: list[str | int],
            default: str | int,
            client_sync: bool = False):
        """
        Parameters
        ----------
        identifier : str
            The ID of this entity property. Must be unique within the entity.
        values : list[str | int]
            The list of values which this entity property can have. This is an
            arbitrary list, containing whatever values you'd like it to have.
        default : str | int
            The default value of this entity property.
        client_sync : bool
            Whether this entity property should be synced clientside, or only
            tracked on the server.
        """

        super().__init__(identifier, default, client_sync)
        self._values = values
        """
        This entity property's set of possible values. For an enum property,
        this is an arbitrary list set by the user.
        """
        self._data_type = 'enum'


class Behaviors:
    """
    Class which represents an entity's behavior file.

    Attributes
    ----------
    identifier : str
    is_spawnable : bool
    is_summonable : bool
    is_experimental : bool
    runtime_identifier : str
    """
    def __init__(
            self,
            identifier: str,
            string_variables: dict = None,
            runtime_identifier: str = None):
        """
        Parameters
        ----------
        identifier : str
            The unique ID of this entity, including namespace. If the entity
            has graphics, it must match the ID of an EntityGraphics object,
            representing an entity's resource file.
        string_variables : dict
            A set of string values to match and replace in this behavior JSON
            file when it is written. Likely to be removed in future versions.
        runtime_identifier : str
            The ID of a vanilla Bedrock entity to inherit from. The effects of
            this vary widely depending on the parent entity.
        """

        self.identifier: str = identifier
        """The unique ID of this entity, including namespace."""
        self.is_spawnable: bool = True
        """If True, this entity will have a spawn egg."""
        self.is_summonable: bool = True
        """If True, this entity will be summonable with commands."""
        self.is_experimental: bool = False
        """Uncertain of usage, might enable experimental components."""
        self._bancos: list[str] = []
        """The IDs of the animation controllers which this entity uses."""
        self._animations: list[Animation] = []
        """The behavior pack animations which this entity uses."""
        self._components: list[Component] = []
        """
        The Components in this entity which are not part of a component group,
        and thus always active.
        """
        self._component_groups: list[ComponentGroup] = []
        """The list of ComponentGroups in this entity."""
        self._events: list[Event] = []
        """List of Events in this entity."""
        self._spawn_groups: list[str] = []
        """
        The IDs of the component groups which are added to the entity
        when it spawns.
        """
        self._spawn_randomizers: list[EventRandomizer] = []
        """The EventRandomizers to be used in the spawn event."""
        self._spawn_sequential_events: list[Event] = []
        """The sub-Events to be used in the spawn event."""
        self._properties: list[EntityProperty] = []
        """List of EntityProperties in this entity."""
        self._spawn_properties = {}
        """
        Initial values of this entity's entity properties to set
        when it spawns.\n
        Each key is the ID of an entity property,
        and each value is what the property will be set to."""
        self._lstate_names = {}
        """
        Dict to facilitate connection of nonlinear loop states.\n
        Each key is an arbitrary name given to an lstate.\n
        Each value is a list of strings. Element 0 is always the true
        identifier for the named lstate. The rest of the elements are the IDs
        of states which connect to it.
        """
        self._string_variables = string_variables
        """
        A dict of key-value string pairs. These are searched for and replaced
        in the entity JSON file when it's generated. Likely to be removed in a
        future version.
        """
        self.runtime_identifier = runtime_identifier
        """
        The ID of a vanilla Bedrock entity to inherit from. The effects of
        this vary widely depending on the parent entity.
        """

    def get_json(self) -> dict:
        """
        Builds a JSON-ready dict of these entity behaviors.

        Returns
        -------
        dict
            A JSON-ready object which can be written as
            an entity behavior file.
        """
        # Create vanilla spawn event
        if (
            len(self._spawn_groups) > 0 or
            len(self._spawn_randomizers) > 0 or
            len(self._spawn_sequential_events) > 0 or
            len(self._spawn_properties) > 0
        ):
            spawn_event = self.get_event('minecraft:entity_spawned')
            if spawn_event is None:
                spawn_event = Event('entity_spawned', namespace='minecraft')
                self._events.append(spawn_event)
            spawn_event.add_add_groups(self._spawn_groups)
            spawn_event.add_randomizers(self._spawn_randomizers)
            spawn_event.add_sequential_events(self._spawn_sequential_events)
            spawn_event._set_properties = self._spawn_properties

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
            desc['scripts'] = {'animate': []}
            for n in range(0, len(self._bancos)):
                desc['scripts']['animate'].append({f'banco_{n}': '1'})
                anim_dict[f'banco_{n}'] = self._bancos[n]
        if len(self._animations) > 0:
            for anim in self._animations:
                anim_dict[anim.identifier] = anim.identifier
        if len(anim_dict) > 0:
            desc['animations'] = anim_dict
        if len(self._properties) > 0:
            prop_obj = {}
            for prop in self._properties:
                prop_obj['property:'+prop.identifier] = prop.get_json()
            desc['properties'] = prop_obj
        entity_obj['description'] = desc

        # Make main bvr sections
        components = {}
        for c in self._components:
            components['minecraft:' + c.comp_type] = c.json_obj
        entity_obj['components'] = components

        if len(self._component_groups) > 0:
            component_groups = {}
            for g in self._component_groups:
                component_groups[g.get_id()] = g.get_json()
            entity_obj['component_groups'] = component_groups

        if len(self._events) > 0:
            events = {}
            for e in self._events:
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
        if self._string_variables is not None:
            replace_obj_string_variables(obj, self._string_variables)

        # Behavior creation complete
        return obj

    def add_banco(self, banco: str) -> None:
        """
        Register a behavior animation controller for use by this entity.

        Parameters
        ----------
        banco : str
            The ID of the banco to use.
        """
        self._bancos.append(banco)

    def add_animation(self, animation: Animation) -> None:
        """
        Add a behavior pack animation to this entity.

        Parameters
        ----------
        animation : Animation
            The animation to add.
        """
        self._animations.append(animation)

    def get_event(self, event_id: str) -> Event | None:
        """
        Searches for an Event in this entity.

        Parameters
        ----------
        event_id : str
            The ID of the Event to search for.

        Returns
        -------
        Event | None
            An Event if one with the ID event_id is found, otherwise None.
        """
        for i in self._events:
            if i.get_id() == event_id:
                return i
        return None

    def add_property(self, prop: EntityProperty) -> None:
        """
        Add an EntityProperty to this entity.

        Parameters
        ----------
        prop : EntityProperty
            The EntityProperty to add.
        """
        self._properties.append(prop)

    def get_component(self, component_id) -> Component | None:
        """
        Searches for an always-active (not inside a component group) Component
        in this entity.

        Parameters
        ----------
        component_id : str
            The ID of the Component to search for.

        Returns
        -------
        Component | None
            A Component if one with the ID component_id is found,
            otherwise None.
        """
        for i in self._components:
            if i.comp_type == component_id:
                return i
        return None


class AnimationController:
    """
    Class which represents an animation controller (anco), for use in either a
    resource pack (ranco) or behavior pack (banco).

    Attributes
    ----------
    identifier : str
    initial_state : str
    """
    def __init__(
            self,
            identifier: str,
            initial_state: str = 'init',
            string_variables: dict = None):
        """
        Parameters
        ----------
        identifier : str
            The unique ID of this animation controller.
        initial_state : str
            The ID of the AncoState which this anco will start in.
        string_variables : dict
            A set of string values to match and replace in this behavior JSON
            file when it is written. Likely to be removed in future versions.
        """

        self.identifier: str = identifier
        """The unique ID of this animation controller."""
        self._states: list[AncoState] = []
        """All of the anco states in this animation controller."""
        self._string_variables: dict = string_variables
        """
        A dict of key-value string pairs. These are searched for and replaced
        in the JSON file when it's generated. Likely to be removed in a
        future version.
        """
        self.initial_state: str = initial_state
        """The ID of the AncoState which this anco will start in."""

    def get_json(self) -> dict:
        """
        Builds a JSON-ready dict of this animation controller.

        Returns
        -------
        dict
            A JSON-ready object which can be written as
            an animation controller file.
        """
        obj = {}
        obj['format_version'] = BANCO_FORMAT_VERSION
        banco = {}
        banco['initial_state'] = self.initial_state
        banco_states = {}

        for i in self._states:
            banco_states[i.identifier] = i.get_json()

        banco['states'] = banco_states
        obj['animation_controllers'] = {}
        obj['animation_controllers'][self.identifier] = banco

        if self._string_variables is not None:
            replace_obj_string_variables(obj, self._string_variables)

        return obj

    def add_state(self, state: AncoState) -> None:
        """
        Add an AncoState to this entity.

        Parameters
        ----------
        prop : AncoState
            The AncoState to add.
        """
        self._states.append(state)

    def add_states(self, states: list[AncoState]) -> None:
        """
        Add a set of AncoStates to this entity.

        Parameters
        ----------
        prop : list[AncoState]
            The AncoStates to add.
        """
        for s in states:
            self.add_state(s)

    def has_state(self, state_name: str) -> bool:
        """
        Checks whether an AncoState of state_name exists in this
        animation controller.

        Parameters
        ----------
        state_name : str
            The ID of the AncoState to search for.

        Returns
        -------
        bool
            True if an AncoState with state_name exists in this animation
            controller, otherwise False.
        """
        for i in self._states:
            if i.identifier == state_name:
                return True
        return False

    def get_state(self, state_name: str) -> AncoState | None:
        """
        Searches for an AncoState in this animation controller.

        Parameters
        ----------
        state_name : str
            The ID of the AncoState to search for.

        Returns
        -------
        AncoState | None
            An AncoState if one with the ID state_name is found,
            otherwise None.
        """
        for i in self._states:
            if i.identifier == state_name:
                return i
        return None


class EntityGraphics:
    """
    Class which represents an entity's resource file.

    Attributes
    ----------
    identifier : str
    material : str
    render_controller : str
    egg_color_1 : str
    egg_color_2 : str
    invisible : bool
    scale : float
    """
    def __init__(
            self,
            identifier: str,
            string_variables: dict = None,
            material: str = 'basic',
            render_controller: str = 'controller.render.default_controller',
            egg_color_1: str = '#550077',
            egg_color_2: str = '#88cc88',
            texture_path: str | dict = None,
            invisible: bool = False,
            geo: str | dict = None,
            animations: dict = None,
            animate_list: list[str] = None,
            particles: dict = None):
        """
        Parameters
        ----------
        identifier : str
            The unique ID of this entity, including namespace. This must match
            the ID of a Behaviors object, representing an entity's
            behavior file.
        string_variables : dict
            A set of string values to match and replace in this behavior JSON
            file when it is written. Likely to be removed in future versions.
        material : str
            The ID of the material this entity will use for rendering.
        render_controller : str
            The ID of the render controller this entity will use for rendering.
        egg_color_1 : str
            The primary color of this entity's spawn egg. It makes up the bulk
            of the texture.
        egg_color_2 : str
            The secondary color of this entity's spawn egg. It determines the
            color of the spawn egg's spots.
        texture_path : str | dict
            The file path of the texture this entity will use. Can be given a
            dict of possible textures, allowing for runtime texture switching.
            If None, one will be created from the identifier, in the format of
            'textures/entity/identifier'.
            If a string, 'texture/entity/' will be prepended automatically for
            convenience.
            If a dict, each value will be set to its key prepended with
            'texture/entity/'.
        invisible : bool
            If true, the entity will not be rendered.
        geo : str | dict
            The ID of the geometry this entity will use. Can be given a
            dict of possible geometries, allowing for runtime geo switching.
            If None, one will be created from the identifier, in the format of
            'geometry.identifier'.
            If a string, 'geometry.' will be prepended automatically for
            convenience.
            If a dict, each value will be set to its key prepended with
            'geometry.'.
        animations : dict
            The animations and animation controllers available for this entity
            to use. Each key is an arbitrary name unique within this entity
            which can be used by the animate list and animation controllers.
            Each value is the ID of an animation or animation controller.
        animate_list : list[str]
            The animations and animation controllers for this entity to run
            constantly. These must correspond to the arbitrary keys in the
            animation dict, not to actual animation or anco IDs.
        particles : dict
            The particles available for this entity to use. Each key is an
            arbitrary name unique within this entity which can be used by the
            animations. Each value is the ID of a particle.
        """

        self.identifier: str = identifier
        """
        The unique ID of this entity, including namespace. This must match
        the ID of a Behaviors object, representing an entity's
        behavior file.
        """
        self.material: str = material
        """The ID of the material this entity will use for rendering."""
        self.render_controller: str = render_controller
        """
        The ID of the render controller this entity will use for rendering.
        """
        self.egg_color_1: str = egg_color_1
        """
        The primary color of this entity's spawn egg. It makes up the bulk
        of the texture.
        """
        self.egg_color_2: str = egg_color_2
        """
        The secondary color of this entity's spawn egg. It determines the
        color of the spawn egg's spots.
        """
        self.invisible: bool = invisible
        """If true, the entity will not be rendered."""
        self.scale: float = 1.0
        """
        The scale to render this entity at. Its visual size will be multiplied
        by this value.
        """
        self.init_list: list[str] = None
        """
        A list of Molang expressions to initialize variables in this entity.
        """
        self.pre_anim: list[str] = None
        """
        A list of Molang expressions to set variables before processing
        animations each tick.
        """

        self._anim_obj: dict = animations
        """
        The animations and animation controllers available for this entity
        to use. Each key is an arbitrary name unique within this entity
        which can be used by _animate_list and animation controllers.
        Each value is the ID of an animation or animation controller.
        """
        self._animate_list: list[str] = animate_list
        """
        The animations and animation controllers for this entity to run
        constantly. These must correspond to the arbitrary keys in the
        _anim_obj, not to actual animation or anco IDs.
        """
        self._string_variables: dict = string_variables
        """
        A dict of key-value string pairs. These are searched for and replaced
        in the entity JSON file when it's generated. Likely to be removed in a
        future version.
        """
        self._particle_obj: dict = particles
        """
        The particles available for this entity to use. Each key is an
        arbitrary name unique within this entity which can be used by the
        animations. Each value is the ID of a particle.
        """

        self.texture_path: str | dict
        """
        The file path of the texture this entity will use. Can also be a
        dict of possible textures, allowing for runtime texture switching.
        If a dict, the keys are arbitrary names usable by render controllers,
        and the values are the texture paths.
        """
        if texture_path is None:
            self.texture_path = 'textures/entity/' + self.identifier
        elif type(texture_path) is str:
            self.texture_path = 'textures/entity/' + texture_path
        elif type(texture_path) is dict:
            self.texture_path = texture_path
            for key in self.texture_path.keys():
                p = self.texture_path[key]
                self.texture_path[key] = 'textures/entity/' + p

        self.geo: str | dict
        """
        The ID of the geometry this entity will use. Can be a
        dict of possible geometries, allowing for runtime geo switching.
        If a dict, the keys are arbitrary names usable by render controllers,
        and the values are the geometry IDs.
        """
        if geo is None:
            self.geo = 'geometry.' + self.identifier
        elif type(geo) is str:
            self.geo = 'geometry.' + geo
        elif type(geo) is dict:
            self.geo = geo
            for key in self.geo.keys():
                self.geo[key] = 'geometry.' + self.geo[key]

    def add_animations(self, anim_obj: dict) -> None:
        """
        Add animations to be usable by this entity.

        Parameters
        ----------
        anim_obj : dict
            The animation to add. Each key is an arbitrary name used by
            the the animate list and animation controllers, and each value is
            the ID of an animation.
        """
        if self._anim_obj is None:
            self._anim_obj = anim_obj
        else:
            self._anim_obj.update(anim_obj)

    def add_particles(self, obj: dict) -> None:
        """
        Add particles to be usable by this entity.

        Parameters
        ----------
        anim_obj : dict
            The animation to add. Each key is an arbitrary name used by
            animations, and each value is the ID of a particle.
        """
        if self.particle_obj is None:
            self.particle_obj = obj
        else:
            self.particle_obj.update(obj)

    def add_animate_list(self, animate_list: list[str]) -> None:
        """
        Set additional animations and/or animation controllers for this entity
        to run by default.

        Parameters
        ----------
        animate_list : list[str]
            The animations and/or animation controllers to run. These must be
            the arbitrary names set in the entity resource file, not the actual
            IDs of the anims and ancos.
        """
        if self._animate_list is None:
            self._animate_list = animate_list
        else:
            self._animate_list.extend(animate_list)

    def add_script_initialize(self, init_list: list[str]) -> None:
        """
        Add Molang initialization expressions.

        Parameters
        ----------
        init_list : list[str]
            The Molang expressions to be run when the entity initializes.
        """
        if self.init_list is None:
            self.init_list = init_list
        else:
            self.init_list.extend(init_list)

    def add_script_pre_anim(self, pre_anim: list[list]) -> None:
        """
        Add Molang expressions to run before processing animations each tick.

        Parameters
        ----------
        pre_anim : list[str]
            The Molang expressions to be run.
        """
        if self.pre_anim is None:
            self.pre_anim = pre_anim
        else:
            self.pre_anim.extend(pre_anim)

    def add_ranco(self, ranco: AnimationController) -> None:
        """
        Register an animation controller to run by default in this entity. It
        will be added to the animation dict as well as the animate list.

        Parameters
        ----------
        ranco : AnimationController
            The animation controller to be run.
        """
        self.add_animations({ranco.identifier: ranco.identifier})
        self.add_animate_list([ranco.identifier])

    def add_humanoid_animations(self) -> None:
        """
        Adds a large set of animations, animation controllers, and
        variable-setting Molang expressions, which set the entity up to use
        vanilla humanoid animations.
        """
        root_a = 'animation.'
        root_p = 'animation.player.'
        root_pf = 'animation.player.first_person.'
        root_h = 'animation.humanoid.'
        root_c = 'controller.animation.'
        root_cp = 'controller.animation.player.'
        self.add_animations({
            "root": root_c+"humanoid.root",
            "base_controller": root_cp+"base",
            "hudplayer":  root_c+"humanoid.hudplayer",
            "humanoid_base_pose": root_h+"base_pose",
            "look_at_target": root_c+"humanoid.look_at_target",
            "look_at_target_ui": root_p+"look_at_target.ui",
            "look_at_target_default": root_h+"look_at_target.default",
            "look_at_target_gliding": root_h+"look_at_target.gliding",
            "look_at_target_swimming": root_h+"look_at_target.swimming",
            "look_at_target_inverted": root_p+"look_at_target.inverted",
            "cape": root_p+"cape",
            "move.arms": root_p+"move.arms",
            "move.legs": root_p+"move.legs",
            "swimming": root_p+"swim",
            "swimming.legs": root_p+"swim.legs",
            "riding.arms": root_p+"riding.arms",
            "riding.legs": root_p+"riding.legs",
            "holding": root_p+"holding",
            "brandish_spear": root_h+"brandish_spear",
            "charging": root_h+"charging",
            "attack.positions": root_p+"attack.positions",
            "attack.rotations": root_p+"attack.rotations",
            "sneaking": root_p+"sneaking",
            "bob": root_p+"bob",
            "damage_nearby_mobs": root_h+"damage_nearby_mobs",
            "fishing_rod": root_h+"fishing_rod",
            "use_item_progress": root_h+"use_item_progress",
            "skeleton_attack": root_a+"skeleton.attack",
            "sleeping": root_p+"sleeping",
            "first_person_base_pose": root_pf+"base_pose",
            "first_person_empty_hand": root_pf+"empty_hand",
            "first_person_swap_item": root_pf+"swap_item",
            "first_person_attack_controller": root_cp+"first_person_attack",
            "first_person_attack_rotation": root_pf+"attack_rotation",
            "first_person_attack_rotation_item": root_pf+"attack_rotation",
            "first_person_vr_attack_rotation": root_pf+"vr_attack_rotation",
            "first_person_walk": root_pf+"walk",
            "first_person_map_controller": root_cp+"first_person_map",
            "first_person_map_hold": root_pf+"map_hold",
            "first_person_map_hold_attack": root_pf+"map_hold_attack",
            "first_person_map_hold_off_hand": root_pf+"map_hold_off_hand",
            "first_person_map_hold_main_hand": root_pf+"map_hold_main_hand",
            "first_person_crossbow_equipped": root_pf+"crossbow_equipped",
            "third_person_crossbow_equipped": root_p+"crossbow_equipped",
            "third_person_bow_equipped": root_p+"bow_equipped",
            "crossbow_hold": root_p+"crossbow_hold",
            "crossbow_controller": root_cp+"crossbow",
            "shield_block_main_hand": root_p+"shield_block_main_hand",
            "shield_block_off_hand": root_p+"shield_block_off_hand",
            "blink": root_c+"persona.blink"
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
            (
                "variable.attack_body_rot_y"
                " = Math.sin(360*Math.sqrt(variable.attack_time))"
                " * 5.0;"
            ),
            (
                "variable.tcos0"
                " = (math.cos(query.modified_distance_moved * 38.17)"
                " * query.modified_move_speed / variable.gliding_speed_value)"
                " * 57.3;"
            )
        ])

    def get_json(self) -> dict:
        """
        Builds a JSON-ready dict of this entity resource definition.

        Returns
        -------
        dict
            A JSON-ready object which can be written as
            an entity resource file.
        """
        obj = {}
        obj['format_version'] = ENTITY_GRAPHICS_FORMAT_VERSION

        desc = {}
        desc['identifier'] = self.identifier
        if not self.invisible:
            desc['materials'] = {'default': self.material}
            desc['render_controllers'] = [self.render_controller]

            if type(self.geo) is str:
                desc['geometry'] = {'default': self.geo}
            elif type(self.geo) is dict:
                desc['geometry'] = self.geo

            if type(self.texture_path) is str:
                desc['textures'] = {'default': self.texture_path}
            elif type(self.texture_path) is dict:
                desc['textures'] = self.texture_path

        else:
            desc['geometry'] = {'default': 'geometry.humanoid'}

        desc['spawn_egg'] = {
            'base_color': self.egg_color_1,
            'overlay_color': self.egg_color_2
        }

        if self._anim_obj is not None:
            desc['animations'] = self._anim_obj

        if self._particle_obj is not None:
            desc['particle_effects'] = self._particle_obj

        script_obj = {'scale': str(self.scale)}
        if self._animate_list is not None:
            script_obj['animate'] = self._animate_list
        if self.init_list is not None:
            script_obj['initialize'] = self.init_list
        if self.pre_anim is not None:
            script_obj['pre_animation'] = self.pre_anim
        desc['scripts'] = script_obj

        obj['minecraft:client_entity'] = {'description': desc}

        if self._string_variables is not None:
            replace_obj_string_variables(obj, self._string_variables)

        return obj


class Entity:
    """
    Class representing an entire Bedrock entity. It contains both an entity's
    Behaviors and EntityGraphics, and tracks data common between them.

    Attributes
    ----------
    namespace : str
    """
    def __init__(
            self,
            namespace: str,
            name: str,
            string_variables: dict = None,
            id: str = None,
            egg_name: str = None,
            collision_x: float = 0,
            collision_y: float = 0,
            hp: int = None,
            attack: int = None,
            move_speed: float = None,
            has_physics: bool = True,
            no_damage: bool = False,
            spawn_groups: list[str] = None,
            has_graphics: bool = False,
            entity_graphics: EntityGraphics = None,
            invisible: bool = False,
            runtime_identifier: str = None,
            despawnable: bool = False,
            ambient_sound: str = None,
            hurt_sound: str = None,
            death_sound: str = None,
            step_sound: str = None,
            sounds_pitch_range: list[float] = [0.8, 1.2],
            sounds_volume: float = 1.0):
        """
        Parameters
        ----------
        namespace : str
            The namespace of this entity.
        name : str
            The display name of this entity. Used to generate an identifier if
            a separate ID is not given.
        string_variables : dict
            A set of string values to match and replace in this behavior JSON
            file when it is written. Likely to be removed in future versions.
        id : str
            The unique ID of this entity.
        egg_name : str
            The display name of this entity's spawn egg.
        collision_x : float
            The horizontal size of this entity's hitbox,
            on both the X and Z axes.
        collision_y : float
            The vertical size of this entity's hitbox.
        hp : int
            The maximum health of this entity. One point is 1/2 heart.
        attack : int
            The melee damage of this entity.
        move_speed : float
            How fast this entity walks.
        has_physics : bool
            Whether this entity should collide with things
            and be affected by gravity.
        no_damage : bool
            If true, this entity will not receive damage from any source,
            though it can still be killed with /kill.
        spawn_groups : list[str]
            The component groups this entity should spawn with enabled.
        has_graphics : bool
            If has_graphics is True and entity_graphics is not provided, an
            EntitGraphics object will be generated for this entity in
            __init__().
        entity_graphics : EntityGraphics
            The EntityGraphics object for this Entity to use.
        invisible : bool
            If true, this entity will not render.
        runtime_identifier : str
            The ID of a vanilla Bedrock entity to inherit from. The effects of
            this vary widely depending on the parent entity.
        ambient_sound : str
            The ID of a sound this entity will play on occasion at random.
        hurt_sound : str
            The ID of a sound this entity will play when it takes damage.
        death_sound : str
            The ID of the sound this entity will play when it dies.
        step_sound : str
            The ID of a sound this entity will play as it walks.
        sounds_pitch_range : list[float]
            The pitch range for all of this entity's sounds. Must be a list of
            two floats, a minimum and maximum value. For example:
                [0.8, 1.2]
            When a sound is played, it will be at a random pitch between these
            values.
        sounds_volume : float
            The volume to play all this entity's sounds at. How exactly this
            works is strange, so you may need to fiddle with it to get the
            results you need.
        """

        self.namespace: str = namespace
        """The namespace of this entity."""
        self.name: str = name
        """The display name of this entity."""
        self._bancos: list[AnimationController] = []
        """All behavior pack animation controllers this entity uses."""
        self._current_state = 0
        """The number of the currently active loop state."""
        self.rancos: list[AnimationController] = []
        """All resource pack animation controllers this entity uses."""

        self.ambient_sound = ambient_sound
        """The ID of a sound this entity will play on occasion at random."""
        self.hurt_sound = hurt_sound
        """The ID of a sound this entity will play when it takes damage."""
        self.death_sound = death_sound
        """The ID of the sound this entity will play when it dies."""
        self.step_sound = step_sound
        """The ID of a sound this entity will play as it walks."""
        self.sounds_pitch_range = sounds_pitch_range
        """
        The pitch range for all of this entity's sounds. Must be a list of
        two floats, a minimum and maximum value. For example:
            [0.8, 1.2]
        When a sound is played, it will be at a random pitch between these
        values.
        """
        self.sounds_volume = sounds_volume
        """
        The volume to play all this entity's sounds at. How exactly this
        works is strange, so you may need to fiddle with it to get the
        results you need.
        """

        self.identifier: str
        """The unique ID of this entity."""
        if id is not None:
            self.identifier = id
        else:
            self.identifier = name.lower().replace(' ', '_')

        self.egg_name: str
        """The display name of this entity's spawn egg."""
        if egg_name is not None:
            self.egg_name = egg_name
        else:
            self.egg_name = 'Spawn ' + name

        self.string_variables = string_variables
        """
        A set of string values to match and replace in this behavior JSON
        file when it is written. Likely to be removed in future versions.
        """

        self.graphics: EntityGraphics
        """This entity's resource pack definition."""
        if entity_graphics is not None:
            self.graphics = entity_graphics
        elif has_graphics:
            self.graphics = EntityGraphics(
                self.get_id(),
                string_variables=self.string_variables,
                invisible=invisible
            )
        else:
            self.graphics = None

        self.behaviors = Behaviors(
            self.get_id(),
            self.string_variables,
            runtime_identifier
        )
        """This entity's behavior pack definition."""

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

    def get_id(self) -> str:
        """
        Returns the complete entity identifier, including namespace.

        Returns
        -------
        str
            The full ID of this entity.
        """
        return self.namespace + ':' + self.identifier

    def add_component(self, component: Component) -> None:
        """
        Add a component to this Entity's behaviors.

        Parameters
        ----------
        component : Component
            The Component to add.
        """
        self.behaviors._components.append(component)

    def add_component_list(self, comp_list: list[Component]) -> None:
        """
        Add a set of components to this Entity's behaviors.

        Parameters
        ----------
        comp_list : list[Component]
            The Components to add.
        """
        for c in comp_list:
            self.add_component(c)

    def add_component_group(self, group: ComponentGroup) -> None:
        """
        Add a component group to this Entity's behaviors.

        Parameters
        ----------
        group : ComponentGroup
            The ComponentGroup to add.
        """
        self.behaviors._component_groups.append(group)

    def add_event(self, event: Event) -> None:
        """
        Add an event to this Entity's behaviors.

        Parameters
        ----------
        event : Event
            The Event to add.
        """
        self.behaviors._events.append(event)

    def create_banco(self, banco_name: str, initial_state: str = None) -> int:
        """
        Create and add a new behavior pack animation controller in this entity.

        Parameters
        ----------
        banco_name : str
            The name of the new banco. It does not require any naming
            boilerplate, and will be automatically prepended with
            'controller.animation.' and the entity's name, to ensure it's
            a valid name and unique between entities.
        initial_state : str
            If provided, the banco will initialize into a state with this
            name instead of the default one.

        Returns
        -------
        int
            The index of this banco within the Entity's banco list.
        """
        banco = AnimationController(
            'controller.animation.' + self.identifier + '_' + banco_name,
            initial_state=initial_state,
            string_variables=self.string_variables
        )
        self._bancos.append(banco)

        if self.behaviors is not None:
            self.behaviors.add_banco(banco.identifier)
        else:
            print('WARNING: banco added to an entity which has no Behaviors.')

        return len(self._bancos)-1

    def add_banco(self, banco: AnimationController) -> int:
        """
        Add a new behavior pack animation controller in this entity.

        Parameters
        ----------
        banco : AnimationController
            The animation controller to add.

        Returns
        -------
        int
            The index of this banco within the Entity's banco list.
        """
        self._bancos.append(banco)
        if self.behaviors is not None:
            self.behaviors.add_banco(banco.identifier)
        else:
            print('WARNING: banco added to an entity which has no Behaviors.')
        return len(self._bancos)-1

    def create_ranco(self, ranco_name: str, initial_state: str = None) -> int:
        """
        Create and add a new resource pack animation controller in this entity.

        Parameters
        ----------
        ranco_name : str
            The name of the new ranco. It does not require any naming
            boilerplate, and will be automatically prepended with
            'controller.animation.' and the entity's name, to ensure it's
            a valid name and unique between entities.
        initial_state : str
            If provided, the ranco will initialize into a state with this
            name instead of the default one.

        Returns
        -------
        int
            The index of this ranco within the Entity's ranco list.
        """
        ranco = AnimationController(
            'controller.animation.' + self.identifier + '_' + ranco_name,
            initial_state=initial_state,
            string_variables=self.string_variables
        )
        self.rancos.append(ranco)

        if self.graphics is not None:
            self.graphics.add_ranco(ranco)
        else:
            print('WARNING: ranco added to entity without graphics')

        return len(self.rancos)-1

    def add_ranco(self, ranco: AnimationController) -> int:
        """
        Add a new resource pack animation controller in this entity.

        Parameters
        ----------
        ranco : AnimationController
            The animation controller to add.

        Returns
        -------
        int
            The index of this ranco within the Entity's ranco list.
        """
        self.rancos.append(ranco)
        if self.graphics is not None:
            self.graphics.add_ranco(ranco)
        else:
            print('WARNING: ranco added to entity without graphics')
        return len(self.rancos)-1

    def add_banco_state(self, banco_idx: int, state: AncoState) -> None:
        """
        Add an AncoState to a banco in this Entity's banco list.

        Parameters
        ----------
        banco_idx : int
            The index of the banco within the Entity's banco list.
        state : AncoState
            The animation controller state to add.
        """
        self._bancos[banco_idx].add_state(state)

    def add_ranco_state(self, ranco_idx: int, state: AncoState) -> None:
        """
        Add an AncoState to a ranco in this Entity's ranco list.

        Parameters
        ----------
        ranco_idx : int
            The index of the ranco within the Entity's ranco list.
        state : AncoState
            The animation controller state to add.
        """
        self.rancos[ranco_idx].add_state(state)

    def add_spawn_group(self, group: str) -> None:
        """
        Set an additional component group to be enabled in the Entity's
        behaviors on spawn.

        Parameters
        ----------
        group : str
            The ID of the component group to enable.
        """
        self.behaviors._spawn_groups.append(group)

    def add_spawn_groups(self, groups: list[str]) -> None:
        """
        Set an additional list of component group to be enabled in the Entity's
        behaviors on spawn.

        Parameters
        ----------
        groups : list[str]
            The IDs of the component groups to enable.
        """
        for i in groups:
            self.behaviors._spawn_groups.append(i)

    def set_identifier(self, id: str) -> None:
        """
        Set the ID of this Entity, and copy it into this Entity's Behaviors
        and EntityGraphics.

        Parameters
        ----------
        id : str
            This entity's new ID.
        """
        self.identifier = id
        self.behaviors.identifier = self.get_id()
        if self.graphics is not None:
            self.graphics.identifier = self.get_id()

    def current_lstate(self) -> str:
        """
        Get the ID of the currently active loop state.

        Returns
        -------
        str
            The ID of the currently active loop state.
        """
        return 'state_' + str(self._current_state)

    def next_lstate(self) -> str:
        """
        Get the ID of the next loop state.

        Returns
        -------
        str
            The ID of the next loop state.
        """
        return 'state_' + str(self._current_state+1)

    def prev_lstate(self) -> str:
        """
        Get the ID of the previous loop state.

        Returns
        -------
        str
            The ID of the previous loop state.
        """
        return 'state_' + str(self._current_state-1)

    def add_loop_state(
            self,
            banco_id: int = 0,
            ranco_id: int = 0,
            components: list[Component] = None,
            entry_commands: list[str] = None,
            exit_commands: list[str] = None,
            timer_len: float = None,
            last_state: bool = False,
            name: str = None,
            connection_list: list[str] = None,
            timer_state: str = None,
            hp: int = None,
            attack: int = None,
            move_speed: float = None,
            no_damage: bool = False,
            animation: str = None,
            end_anim_with_state: bool = True,
            anim_blend_time: float = 0.2,
            set_properties: dict = None) -> None:
        """
        Parameters
        ----------
        banco_id : int
            The index of the banco in this Entity's banco list which this loop
            state will use.
        ranco_id : int
            The index of the ranco in this Entity's ranco list which this loop
            state will use.
        components : list[Component]
            The Components which will be in this loop state's component group.
            Avoid adding redundant Components which are already added by using
            other parameters in this method.
        entry_commands : list[str]
            The commands which will be executed when
            this loop state is entered.
        exit_commands : list[str]
            The commands which will be executed when this loop state is exited.
        time_len : float
            If used, this loop state will end after time_len seconds.
        last_state : bool
            Must be set to True if this is the last state in the sequence, or
            it will not loop back to the start.
        name : str
            The ID of this loop state, for use in creating non-linear
            connections.
        connection_list : list[str]
            A list of the names of all other loop states which connect to this
            one in a non-linear way.
        timer_state : str
            The name of the loop state to transition into when time_len reaches
            0, if a branching connection is desired.
        hp : int
            The entity's max health while it's in this loop state. 1 point is
            1/2 heart.
        attack : int
            The entity's melee damage while it's in this loop state.
        move_speed : float
            The entity's walk speed while it's in this loop state.
        no_damge : bool
            If true, the entity will be unable to take damage while in this
            loop state. It can still be killed with /kill.
        animation : str
            The name of an animation or ranco to play while in this loop state.
            Note that this is one of the arbitrary name set in the resource
            file, not an actual ID.
        end_anim_with_state : bool
            If true, forces the animation to end when the loop state does. If
            false, the animation will end when the animation itself finishes.
        anim_blend_time : float
            The time in seconds to blend between this loop state's animation
            and the animation it transitions into.
        set_properties : dict
            The entity properties to set when this loop state is entered. Each
            key is the ID of an entity property, and each value is what to set
            it to.
        """

        group = ComponentGroup(
            self.current_lstate(),
            skin_id=self._current_state
        )
        if timer_len is not None:
            if timer_state is not None:
                group.add_component(component_timer(timer_len, timer_state))
                if connection_list is None:
                    connection_list = [timer_state]
                else:
                    connection_list.append(timer_state)
            elif not last_state:
                group.add_component(component_timer(
                    timer_len,
                    self.next_lstate()
                ))
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
            banco_state.add_transition(
                'init',
                'query.skin_id!='+str(self._current_state)
            )
            if entry_commands is not None:
                for i in entry_commands:
                    banco_state.add_entry_command(i)
            if exit_commands is not None:
                for i in exit_commands:
                    banco_state.add_exit_command(i)
            self.add_banco_state(banco_id, banco_state)

            self._bancos[banco_id].initial_state = 'init'
            if not self._bancos[banco_id].has_state('init'):
                self.add_banco_state(banco_id, AncoState('init'))
            self._bancos[banco_id].get_state('init').add_transition(
                self.current_lstate(),
                'query.skin_id=='+str(self._current_state)
            )

        if animation is not None:
            ranco_state = AncoState(self.current_lstate())
            if end_anim_with_state:
                ranco_state.add_transition(
                    'init',
                    'query.skin_id!='+str(self._current_state)
                )
            else:
                ranco_state.add_transition(
                    'init',
                    'query.all_animations_finished'
                )
            ranco_state.add_animation(animation)
            ranco_state._transition_time = anim_blend_time
            self.add_ranco_state(ranco_id, ranco_state)

            self.rancos[ranco_id].initial_state = 'init'
            if not self.rancos[ranco_id].has_state('init'):
                self.add_ranco_state(ranco_id, AncoState('init'))
            self.rancos[ranco_id].get_state('init').add_transition(
                self.current_lstate(),
                'query.skin_id=='+str(self._current_state)
            )

        if self._current_state == 0 and set_properties is not None:
            self.behaviors._spawn_properties.update(set_properties)

        event = Event(
            self.current_lstate(),
            add_groups=[self.current_lstate()],
            remove_groups=[self.prev_lstate()]
        )
        if set_properties is not None:
            event._set_properties = set_properties
        self.add_event(event)
        if last_state:
            for i in self.behaviors._events:
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

        self._current_state += 1

    def get_sounds_obj(self) -> dict:
        """
        Compile a JSON-ready dict of this entity's basic sounds.

        Returns
        -------
        dict
            A JSON-ready dict ready to write into a sound definition file.
        """
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
        id: str,
        entity_graphics: EntityGraphics,
        damage: int,
        namespace: str,
        string_variables: dict = None,
        name: str = None,
        collision_box_size: float = 0.25,
        knockback: bool = True,
        enflame: bool = False,
        spawn_entity: str = None,
        spawn_chance: float = 100.0,
        spawn_count: int = 1,
        hit_sound: str = 'bow.hit',
        stick_in_ground: bool = False,
        destroyed_on_hit: bool = True,
        spread: int = 10,
        power: float = 1.0,
        gravity: float = 0.05,
        remove_on_hit: bool = False) -> Entity:
    """
    Creates an Entity which can be used as a projectile.

    Parameters
    ----------
    id : str
        The unique ID of this entity.
    entity_graphics : EntityGraphics
        The graphics definition of this projectile.
    damage : int
        How much damage this projectile will do on impact.
        1 point is 1/2 heart.
    namespace : str
        The namespace this entity will use.
    string_variables : dict
        A set of string values to match and replace in this behavior JSON
        file when it is written. Likely to be removed in future versions.
    name : str
        An optional display name for this entity. If not provided, it will just
        use its ID.
    collision_box_size : float
        The size of this projectile's collision box. Applies to all 3 axes.
    knockback : bool
        If true, this projectile will induce knockback when it hits.
    enflame : bool
        If true, this projectile will set entities it hits on fire.
    spawn_entity : str
        The ID (not including namespace) of an entity to spawn when this
        projectile impacts something.
    spawn_chance : float
        The percent change that spawn_entity will be spawned.
    spawn_count : int
        The number of spawn_entity to spawn on impact.
    hit_sound : str
        The sound this projectile will make when it hits something.
    stick_in_ground : bool
        If true, this projectile will persist in the block
        it hits after impact.
    destroyed_on_hit : bool
        If true, this projectile will be deleted if it takes damage.
    spread : int
        The degree of randomness applied to this projectile's trajectory
        when fired.
    power : float
        The speed this projectile is fired at.
    gravity : float
        How much gravity is applied to this projectile as it flies.
    remove_on_hit : bool
        Removes the projectile "on hit". Official documentation does not
        explain what this does.
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
        # "multiple_targets": not destroyed_on_hit,
        "hit_sound": hit_sound,
        "power": power,
        "gravity": gravity,
        "uncertainty_base": spread,
        "uncertainty_multiplier": 0,
        "anchor": 1,
        "should_bounce": True,
        # "stop_on_hurt": {},
        "offset": [0, -0.1, 0],
        "catch_fire": enflame
    }

    if stick_in_ground:
        projectile_json_obj['on_hit']['stick_in_ground'] = {"shake_time": 0.35}
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

    projectile_component.json_obj = projectile_json_obj
    entity.add_component(projectile_component)

    # optimizer_component = Component('conditional_bandwidth_optimization')
    # optimizer_json_obj = {
    #     "default_values": {
    #       "max_optimized_distance": 80.0,
    #       "max_dropped_ticks": 10,
    #       "use_motion_prediction_hints": True
    #     }
    # }

    # entity.add_component(optimizer_component)

    return entity
