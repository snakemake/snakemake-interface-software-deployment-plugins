__author__ = "Johannes Köster"
__copyright__ = "Copyright 2024, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

import types
from typing import Mapping
from snakemake_interface_software_deployment_plugins.settings import (
    CommonSettings,
    SoftwareDeploymentProviderSettingsBase,
)

from snakemake_interface_common.plugin_registry.attribute_types import (
    AttributeKind,
    AttributeMode,
    AttributeType,
)
from snakemake_interface_software_deployment_plugins.registry.plugin import Plugin
from snakemake_interface_common.plugin_registry import PluginRegistryBase
from snakemake_interface_software_deployment_plugins import EnvBase, SoftwareDeploymentProviderBase, _common as common


class SoftwareDeploymentPluginRegistry(PluginRegistryBase):
    """This class is a singleton that holds all registered executor plugins."""

    @property
    def module_prefix(self) -> str:
        return common.software_deployment_plugin_module_prefix

    def load_plugin(self, name: str, module: types.ModuleType) -> Plugin:
        """Load a plugin by name."""
        return Plugin(
            _name=name,
            _software_deployment_provider=module.SoftwareDeploymentProvider,
            common_settings=module.common_settings,
            _software_deployment_settings_cls=getattr(module, "SoftwareDeploymentProviderSettings", None),
        )

    def expected_attributes(self) -> Mapping[str, AttributeType]:
        return {
            "SoftwareDeploymentProviderSettings": AttributeType(
                cls=SoftwareDeploymentProviderSettingsBase,
                mode=AttributeMode.OPTIONAL,
                kind=AttributeKind.CLASS,
            ),
            "SoftwareDeploymentProvider": AttributeType(
                cls=SoftwareDeploymentProviderBase,
                mode=AttributeMode.REQUIRED,
                kind=AttributeKind.CLASS,
            ),
            "Env": AttributeType(
                cls=EnvBase,
                mode=AttributeMode.REQUIRED,
                kind=AttributeKind.CLASS,
            )
        }
