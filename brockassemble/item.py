"""
Module containing the Item class, for generating custom in-game items.
"""
import brockassemble.component as comp


ITEM_BVR_FORMAT_VERSION = '1.16.100'


class Item:
    """
    Abstraction of a Bedrock custom item type.

    Attributes
    ----------
    namespace : str
    name : str
    identifier : str
    category : str
    components : list[Component]
    events : list[Component]
    texture_name : str
    """
    def __init__(
            self,
            namespace: str,
            name: str,
            texture_name: str = None,
            id: str = None,
            category: str = 'Items'):
        self.namespace = namespace
        """
        The namespace for this item type, which will be prefixed to
        the item ID.
        This should probably be the same as all other namespaces in your addon.
        """
        self.name = name
        """
        The display name for this item type.
        If the id parameter is not used in __init__, name will be used to
        generate an identifier.
        """
        self.category = category
        """The category of this item type."""
        self.components: list[comp.Component] = []
        """
        A list of all the item components which are part of this item type.
        """
        self.events: list[comp.Component] = []
        """
        A list of all the item events which are part of this item type.
        Currently events are entered as Component objects.
        """
        self.identifier : str
        """The ID for this item type, minus its namespace."""
        if id != None:
            self.identifier = id
        else:
            self.identifier = name.lower().replace(' ', '_')

        self.texture_name: str
        """The file name of the inventory icon this item will use."""
        if texture_name != None:
            self.texture_name = texture_name
        else:
            self.texture_name = self.identifier
        
        # Give the item type its inventory icon
        icon_comp = comp.Component('icon')
        icon_comp.json_obj['texture'] = self.texture_name
        self.components.append(icon_comp)

        # Give the item type its display name
        name_comp = comp.Component('display_name')
        name_comp.json_obj['value'] = self.name
        self.components.append(name_comp)
    
    def get_json(self):
        obj = {}

        obj['format_version'] = ITEM_BVR_FORMAT_VERSION

        desc = {}
        desc['identifier'] = self.get_id()
        desc['category'] = self.category

        comp = {}
        for c in self.components:
            comp['minecraft:' + c.comp_type] = c.json_obj

        event_list = {}
        for e in self.events:
            event_list[e.comp_type] = e.json_obj

        item = {}
        item['description'] = desc
        item['components'] = comp
        item['events'] = event_list
        obj['minecraft:item'] = item

        return obj
    
    def set_texture(self, texid):
        self.texture_name = texid
        icon_comp = comp.Component('icon')
        icon_comp.json_obj['texture'] = self.texture_name
        self.components[0] = icon_comp

    def set_display_name(self, name):
        self.name = name
        name_comp = comp.Component('display_name')
        name_comp.json_obj['value'] = self.name
        self.components[1] = name_comp

    def add_on_use_command(self, command):
        comp = comp.Component('on_use')
        comp.json_obj['on_use'] = { 'event':'on_use', 'target':'self' }
        self.components.append(comp)
        event = comp.Component('on_use')
        event.json_obj['run_command'] = { 'command':[command], 'target':'holder' }
        self.events.append(event)

    def get_id(self):
        return self.namespace + ':' + self.identifier
