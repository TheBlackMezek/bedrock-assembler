import component as component


ITEM_BVR_FORMAT_VERSION = '1.16.100'


class Item:

    def __init__(self, namespace, name, texname=None, id=None, category='Items'):
        self.namespace = namespace
        self.name = name
        self.category = category
        self.components = []
        self.events = []

        if id != None:
            self.identifier = id
        else:
            self.identifier = name.lower().replace(' ', '_')

        if texname != None:
            self.texture_name = texname
        else:
            self.texture_name = self.identifier
        
        icon_comp = component.Component('icon')
        icon_comp.json_obj['texture'] = self.texture_name
        self.components.append(icon_comp)
        name_comp = component.Component('display_name')
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
        icon_comp = component.Component('icon')
        icon_comp.json_obj['texture'] = self.texture_name
        self.components[0] = icon_comp

    def set_display_name(self, name):
        self.name = name
        name_comp = component.Component('display_name')
        name_comp.json_obj['value'] = self.name
        self.components[1] = name_comp

    def add_on_use_command(self, command):
        comp = component.Component('on_use')
        comp.json_obj['on_use'] = { 'event':'on_use', 'target':'self' }
        self.components.append(comp)
        event = component.Component('on_use')
        event.json_obj['run_command'] = { 'command':[command], 'target':'holder' }
        self.events.append(event)

    def get_id(self):
        return self.namespace + ':' + self.identifier
