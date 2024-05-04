# Changelog


## Version 0.2.4 (2024-05-03)

### Additions
* Unit tests for Item class

### Fixes & Improvements
* Turn Item texture_name and name variables into properties to automatically set their related component values
* Remove Item.add_on_use_command() in favor of an Item.on_use_command variable which is compiled into a component and event in Item.get_json().


## Version 0.2.3 (2024-05-02)

### Additions
* pytest unit test folder
* Unit tests for all functions in command.py
* Unit tests for all functions and classes in component.py


## Version 0.2.2 (2023-08-22)

### Additions
* A changelog

### Fixes & Improvements
* Replaced old mentions of .anim_obj and .animate_list in Entity with ._anim_obj and ._animate_list
* The Entity.get_id() docstring now refers to Entity as an entity, not an event
* The init methods for Behaviors and EntityGraphics now take separate namespace and identifier parameters like the rest of the classes
