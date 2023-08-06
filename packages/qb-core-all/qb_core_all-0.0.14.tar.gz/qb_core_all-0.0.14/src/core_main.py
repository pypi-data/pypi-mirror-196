"""
use this module to initialize the whole app

Note setuptools is not picking this up
probably because this module is directly off of src
"""
import qb_core.oproc_pkg.oproc
import qb_core.rats_pkg.rats
import qb_core.ocra_pkg.ocra
from qb_core.common.plugin.peristence import PersistencePluginManager


def initialize_app():
    # since this involves importing, it's good to do this upfront
    PersistencePluginManager.initialize("cook_persistence_interface", "qb_core.rats_pkg.cook.cook_persistence_core")
    print(f'{PersistencePluginManager.get_persistence_implementation("cook_persistence_interface")}')

    qb_core.rats_pkg.rats.initialize_module()
    qb_core.oproc_pkg.oproc.initialize_module()
    qb_core.ocra_pkg.ocra.initialize_module()


