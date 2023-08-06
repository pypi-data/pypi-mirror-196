"""cook_entity.py"""
from qb_core.common.plugin.plugin_manager import PluginManager

"""
this provides cook service
basically all the functions related to cook are included here 
"""
_cook_persistence = None


def initialize():
    global _cook_persistence
    _cook_persistence = PluginManager.get_plugin(
        "cook_persistence_plug_point")


def add_cook(cook):
    # cook specific validations go here
    # example, are all fields correct?
    _cook_persistence.save_cook(cook)


def remove_cook(cook):
    # cook specific validations go here
    _cook_persistence.remove_cook(cook)
