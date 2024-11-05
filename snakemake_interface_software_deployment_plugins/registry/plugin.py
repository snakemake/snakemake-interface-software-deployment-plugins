__author__ = "Johannes Köster"
__copyright__ = "Copyright 2024, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from dataclasses import dataclass
from typing import Optional, Type
from snakemake_interface_software_deployment_plugins.settings import (
    CommonSettings,
    SoftwareDeploymentSettingsBase,
)
import snakemake_interface_software_deployment_plugins._common as common

from snakemake_interface_common.plugin_registry.plugin import PluginBase


@dataclass
class Plugin(PluginBase):
    _software_deployment_provider: object
    common_settings: CommonSettings
    _software_deployment_settings_cls: Optional[Type[SoftwareDeploymentSettingsBase]]
    _name: str

    @property
    def software_deployment_provider(self):
        return self._software_deployment_provider(name=self._only_name)

    @property
    def name(self):
        return self._name

    @property
    def cli_prefix(self):
        return "sdm-" + self._only_name
    
    @property
    def _only_name(self):
        return self.name.replace(common.software_deployment_plugin_module_prefix, "")

    @property
    def settings_cls(self):
        return self._software_deployment_settings_cls
