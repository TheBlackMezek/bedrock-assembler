"""
Module containing the Item class, for generating custom in-game items.
"""
from brockassemble.component import Component


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
        """
        Parameters
        ----------
        namespace : str
            The namespace for this item type, which will be prefixed to
            the item ID. This should probably be the same as all other
            namespaces in your addon.
        name : str
            The display name for this item type.
            If the id parameter is not used in, name will be used to
            generate an identifier.
        texture_name : str
            The file name of the inventory icon this item will use.
        id : str
            The ID for this item type, minus its namespace.
        category : str
            The category of this item type.
        """

        # Components are added first because they are referenced later by
        # property setters.
        self.components: list[Component] = []
        """
        A list of all the item components which are part of this item type.
        """

        self._name_comp = Component('display_name')
        """
        The component which stores the in-game display name of the item.
        Automatically added to the item component list on init.
        """
        self.components.append(self._name_comp)

        self._icon_comp = Component('icon')
        """
        The component which stores the name of the item's icon texture.
        Automatically added to the item component list on init.
        """
        self.components.append(self._icon_comp)

        # Variables and properties can now be set safely.
        self.namespace = namespace
        """
        The namespace for this item type, which will be prefixed to
        the item ID.
        This should probably be the same as all other namespaces in your addon.
        """
        self.name = name
        """
        The display name for this item type.
        """
        self.category = category
        """The category of this item type."""
        self.events: list[Component] = []
        """
        A list of all the item events which are part of this item type.
        Currently events are entered as Component objects.
        """
        self.identifier: str
        """The ID for this item type, minus its namespace."""
        if id is not None:
            self.identifier = id
        else:
            self.identifier = name.lower().replace(' ', '_')

        self.texture_name: str
        """The file name of the inventory icon this item will use."""
        if texture_name is not None:
            self.texture_name = texture_name
        else:
            self.texture_name = self.identifier

    @property
    def texture_name(self):
        return self._texture_name

    @texture_name.setter
    def texture_name(self, value: str):
        self._texture_name = value
        self._icon_comp.json_obj['texture'] = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        self._name_comp.json_obj['value'] = value

    def get_json(self) -> dict:
        """
        Compile this item type's components, events, and other attributes into
        a dict ready for writing as an item's JSON behavior file.
        """
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

    def add_on_use_command(self, command: str) -> None:
        """
        Add a command which the item will execute on "use"
        (right click on desktop).
        """
        comp = Component('on_use')
        comp.json_obj['on_use'] = {'event': 'on_use', 'target': 'self'}
        self.components.append(comp)
        event = Component('on_use')
        event.json_obj['run_command'] = {
            'command': [command], 'target': 'holder'
        }
        self.events.append(event)

    def get_id(self) -> str:
        """
        Get the complete ID of this item type,
        with both namespace and identifier
        """
        return self.namespace + ':' + self.identifier
