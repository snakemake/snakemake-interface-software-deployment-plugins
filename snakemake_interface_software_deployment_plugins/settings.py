from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Sequence, Set

from snakemake_interface_common.settings import SettingsEnumBase, TSettingsEnumBase


import snakemake_interface_common.plugin_registry.plugin


@dataclass
class CommonSettings:
    """Common Snakemake settings shared between executors that can be specified
    by executor plugins.

    The plugin has to specify an instance of this class as the value of the
    common_settings attribute.

    Attributes
    ----------
    
    """
    pass


@dataclass
class SoftwareDeploymentProviderSettingsBase(
    snakemake_interface_common.plugin_registry.plugin.SettingsBase
):
    """Base class for software deployment settings.

    Software deployment plugins can define a subclass of this class,
    named 'SoftwareDeploymentProviderSettings'.
    """

    pass
