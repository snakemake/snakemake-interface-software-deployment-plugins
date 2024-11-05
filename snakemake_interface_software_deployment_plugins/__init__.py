__author__ = "Johannes Köster"
__copyright__ = "Copyright 2024, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod
import hashlib
from pathlib import Path
import sys
from typing import List, Optional, Self

from snakemake_interface_software_deployment_plugins.settings import SoftwareDeploymentProviderSettingsBase


class EnvSpecBase(ABC):
    pass


class EnvBase(ABC):
    def __init__(self, provider: "SoftwareDeploymentProviderBase", spec: EnvSpecBase, parent_env: Optional[Self]):
        self.provider = provider
        self.spec = spec
        self.parent_env = parent_env
        self._managed_hash_store = None
        self._managed_deployment_hash_store = None
        self.__post_init__()

    def __post_init__(self):  # noqa B027
        """Do stuff after object initialization."""
        pass

    @abstractmethod
    def decorate_shellcmd(self, cmd: str) -> str:
        """Decorate given shell command such that it runs within the environment."""
        ...

    @abstractmethod
    def deploy(self):
        """Deploy the environment to self.provider.deployment_path.

        When issuing shell commands, the environment should use
        self.managed_decorate_shellcmd in order to ensure that it runs within eventual
        parent environments (e.g. a container or an env module).
        """
        ...

    @abstractmethod
    def archive(self):
        """Archive the environment to self.provider.archive_path.
        
        When issuing shell commands, the environment should use
        self.managed_decorate_shellcmd in order to ensure that it runs within eventual
        parent environments (e.g. a container or an env module).
        """
        ...

    @abstractmethod
    def hash(self, hash_object) -> None:
        """Update given hash such that it changes whenever the environment
        could potentially contain a different set of software (in terms of versions or
        packages).
        """
        ...

    @abstractmethod
    def deployment_hash(self, hash_object):
        """Update given hash such that it changes whenever the environment 
        needs to be redeployed, e.g. because its content has changed or the 
        deployment location has changed. The latter is only relevant if the
        deployment is senstivive to the path (e.g. in case of conda, which patches
        the RPATH in binaries).
        """
        ...

    def managed_decorate_shellcmd(self, cmd: str) -> str:
        cmd = self.decorate_shellcmd(cmd)
        if self.parent_env is not None:
            cmd = self.parent_env.managed_decorate_shellcmd(cmd)
        return cmd

    def managed_hash(self) -> str:
        return self._managed_generic_hash("hash")
    
    def managed_deployment_hash(self) -> str:
        return self._managed_generic_hash("deployment_hash")

    def _managed_generic_hash(self, kind: str) -> str:
        store = getattr(self, f"_managed_{kind}_store")
        if store is None:
            hash_object = hashlib.md5()
            if self.parent_env is not None:
                hash_object.update(getattr(self.parent_env, kind)().encode())
            getattr(self, kind)(hash_object)
            store = hash_object.hexdigest()
        return store


class SoftwareDeploymentProviderBase(ABC):
    def __init__(
            self,
            name: str,
            prefix: Path,
            settings: Optional[SoftwareDeploymentProviderSettingsBase] = None,
            parent_env: Optional[EnvBase] = None
        ):
        self.settings = settings
        self.deployment_path = prefix / name
        self.archive_path = prefix / f"{name}-archive"
        self.parent_env = parent_env
        self.__post_init__()

    def __post_init__(self):  # noqa B027
        """Do stuff after object initialization, e.g. checking for availability of
        commands.
        """
        pass

    @classmethod
    def get_env_cls(cls):
        provider = sys.modules[cls.__module__]  # get module of derived class
        return provider.Env

    def env(self, spec: EnvSpecBase) -> EnvBase:
        return self.get_env_cls()(provider=self, spec=spec, parent_env=self.parent_env)