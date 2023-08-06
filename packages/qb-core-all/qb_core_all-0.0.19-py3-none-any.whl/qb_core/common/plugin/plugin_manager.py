import importlib

from qb_core.common.plugin.config import core_plug_point_configuration


class PluginManager:
    persistence_obj_dict = {}
    plugin_initialized = False

    # @classmethod
    # def setup_plugins_OLD(cls, persistence_interface_module_name, persistence_impl_module_name):
    #     """
    #     examples
    #     (persistence_interface_module_name="cook_persistence_plug_point", module_name="qb_core.rats_pkg.cook.cook_persistence_core")
    #     (persistence_interface_module_name="cook_persistence_plug_point", module_name="cook.cook_persistence_dynamodb")
    #     :param persistence_interface_module_name:
    #     :param persistence_impl_module_name:
    #     :return:
    #     """
    #     module = importlib.import_module(persistence_impl_module_name)
    #     cls.persistence_obj_dict[persistence_interface_module_name] = module
    #     cls.plugin_initialized = True

    @classmethod
    def get_plugin(cls, persistence_interface_module_name):
        module = cls.persistence_obj_dict.get(persistence_interface_module_name)
        if module is None:
            if cls.plugin_initialized is False:
                msg = 'PluginManager has not been initialized. ' \
                      'Did you forget to call PluginManager.setup_plugins?' \
                      'Or was there an error calling it?'
            else:
                msg = f'there is no module for {persistence_interface_module_name=}. ' \
                      f'Have you defined the right name for the plugin? '
            print(msg)
            raise BaseException(msg)

        return module.get_implementation()

    @classmethod
    def _import_plugins(cls, plug_point_configuration):
        """
        this method is invoked only by core modules.
        infrastructure module are recommended to use override_plugins method.
        :param plug_point_configuration:
        :return:
        """
        # this method imports plugin modules and associates the module to the
        # plug point
        for plug_point, plug_point_dict in plug_point_configuration.items():
            if "plugin" in plug_point_dict:
                print(f'setting up {plug_point=}. we expect a python module of with name {plug_point_dict["plugin"]}')
                module = importlib.import_module(plug_point_dict["plugin"])
                cls.persistence_obj_dict[plug_point] = module
                cls.plugin_initialized = True
            else:
                raise ValueError(f'plugin is not defined for {plug_point=}')

    @classmethod
    def setup_core_plugins(cls):
        """
        this method is invoked only by core modules.
        infrastructure module are recommended to use override_plugins method.
        :return:
        """
        cls._import_plugins(core_plug_point_configuration)

    @classmethod
    def override_plugins(cls, override_plugin_dict):
        """
        infrastructure modules are recommended to use this method to override the plugins
        provided by core.
        see plugin/config.py for the list of plug points declared by the module.
        :param override_plugin_dict:
        :return:
        """
        for plug_point, override_plug_in in override_plugin_dict.items():
            if plug_point in core_plug_point_configuration:
                core_plug_point_configuration[plug_point]["plugin"] = override_plug_in
            else:
                raise ValueError(f'There is no plug_point with name {plug_point} defined in core')
        cls._import_plugins(core_plug_point_configuration)
