from typing import List
from snakemake_interface_software_deployment_plugins.registry import (
    SoftwareDeploymentPluginRegistry,
)
from snakemake_interface_common.plugin_registry.tests import TestRegistryBase
from snakemake_interface_common.plugin_registry.plugin import PluginBase, SettingsBase
from snakemake_interface_common.plugin_registry import PluginRegistryBase


class TestRegistry(TestRegistryBase):
    __test__ = True

    def get_registry(self) -> PluginRegistryBase:
        # ensure that the singleton is reset
        SoftwareDeploymentPluginRegistry._instance = None
        return SoftwareDeploymentPluginRegistry()

    def get_test_plugin_name(self) -> str:
        return "envmodules"

    def validate_plugin(self, plugin: PluginBase):
        assert plugin.settings_cls is None
        assert plugin.env_cls is not None
        assert plugin.env_spec_cls is not None

    def validate_settings(self, settings: SettingsBase, plugin: PluginBase):
        # assert isinstance(settings, plugin.settings_cls)
        pass

    def get_example_args(self) -> List[str]:
        return []
