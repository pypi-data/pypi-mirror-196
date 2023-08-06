"""cook_entity.py"""
from qb_core.common.plugin.peristence import PersistencePluginManager

"""
this provides cook service
basically all the functions related to cook are included here 
"""
_cook_persistence = None


def initialize():
    global _cook_persistence
    _cook_persistence = PersistencePluginManager.get_persistence_implementation(
        "cook_persistence_interface")


def add_cook(cook):
    # cook specific validations go here
    # example, are all fields correct?
    _cook_persistence.save_cook(cook)


def remove_cook(cook):
    # cook specific validations go here
    _cook_persistence.remove_cook(cook)
