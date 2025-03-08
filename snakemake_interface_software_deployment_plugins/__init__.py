__author__ = "Johannes Köster"
__copyright__ = "Copyright 2024, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod
from copy import copy
from dataclasses import dataclass, field
import hashlib
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Self, Tuple, Type, Union
import subprocess as sp

from snakemake_interface_software_deployment_plugins.settings import (
    SoftwareDeploymentSettingsBase,
)


@dataclass
class SoftwareReport:
    name: str
    version: Optional[str] = None
    is_secondary: bool = False


@dataclass
class EnvSpecSourceFile:
    path_or_uri: Union[str, Path]
    cached: Optional[Path] = field(init=False, repr=False, default=None)


class EnvSpecBase(ABC):
    def technical_init(self):
        """This has to be called by Snakemake upon initialization"""
        self.within: Optional["EnvSpecBase"] = None
        self.fallback: Optional["EnvSpecBase"] = None
        self.kind: str = self.__class__.__module__.common_settings.provides
        self._obj_hash: Optional[int] = None

    @classmethod
    def env_cls(cls):
        return cls.__module__.EnvBase

    @classmethod
    @abstractmethod
    def identity_attributes(cls) -> Iterable[str]:
        """Yield the attributes of the subclass that uniquely identify the
        environment spec. These are used for hashing and equality comparison.
        """
        ...

    @classmethod
    @abstractmethod
    def source_path_attributes(cls) -> Iterable[str]:
        """Return iterable of attributes of the subclass that represent paths that are
        supposed to be interpreted as being relative to the defining rule.

        For example, this would be attributes pointing to conda environment files.
        """
        ...

    def has_source_paths(self) -> bool:
        if any(
            getattr(self, attr) is not None for attr in self.source_path_attributes()
        ):
            return True
        if self.within is not None and self.within.has_source_paths():
            return True
        if self.fallback is not None and self.fallback.has_source_paths():
            return True
        return False

    def modify_source_paths(self, modify_func) -> Self:
        if self.has_source_paths():
            self_or_copied = copy(self)
        else:
            return self
        for attr_name in self_or_copied.source_path_attributes():
            current_value = getattr(self_or_copied, attr_name)
            if current_value is not None:
                setattr(self_or_copied, attr_name, modify_func(current_value))

        if self_or_copied.within is not None:
            self_or_copied.within = self_or_copied.within.modify_source_paths(
                modify_func
            )

        if self_or_copied.fallback is not None:
            self_or_copied.fallback = self_or_copied.fallback.modify_source_paths(
                modify_func
            )
        return self_or_copied

    def __or__(self, other: "EnvSpecBase") -> "EnvSpecBase":
        copied = copy(self)
        copied.fallback = other
        copied._obj_hash = None
        return copied

    @classmethod
    def managed_identity_attributes(cls) -> Iterable[str]:
        yield from cls.identity_attributes()
        yield "kind"
        yield "within"
        yield "fallback"

    def __hash__(self) -> int:
        return hash(
            tuple(getattr(self, attr) for attr in self.managed_identity_attributes())
        )

    def __eq__(self, other) -> bool:
        return self.__class__ == other.__class__ and all(
            getattr(self, attr) == getattr(other, attr)
            for attr in self.managed_identity_attributes()
        )


class EnvBase(ABC):
    _cache: Dict[Tuple[Type["EnvBase"], Optional["EnvBase"]], Any] = {}

    def __init__(
        self,
        spec: EnvSpecBase,
        within: Optional["EnvBase"],
        settings: Optional[SoftwareDeploymentSettingsBase],
        shell_executable: str,
        deployment_prefix: Optional[Path] = None,
        archive_prefix: Optional[Path] = None,
    ):
        self.spec: EnvSpecBase = spec
        self.within: Optional["EnvBase"] = within
        self.settings: Optional[SoftwareDeploymentSettingsBase] = settings
        self.shell_executable: str = shell_executable
        self._managed_hash_store: Optional[str] = None
        self._managed_deployment_hash_store: Optional[str] = None
        self._obj_hash: Optional[int] = None
        self._deployment_prefix: Optional[Path] = deployment_prefix
        self._archive_prefix: Optional[Path] = archive_prefix
        self.__post_init__()

    def __post_init__(self) -> None:  # noqa B027
        """Do stuff after object initialization."""
        pass

    @staticmethod
    def once(func):
        """Decorator to cache the result of a method call that shall be only
        executed once per combination of plugin and "within" environment.
        """

        def wrapper(self, *args, **kwargs):
            key = (self.__class__, self.within)
            if key in self._cache:
                return self._cache[key]
            value = func(self, *args, **kwargs)
            self._cache[key] = value
            return value

        return wrapper

    @abstractmethod
    def decorate_shellcmd(self, cmd: str) -> str:
        """Decorate given shell command such that it runs within the environment,
        using self.spec.
        """
        ...

    @abstractmethod
    def record_hash(self, hash_object) -> None:
        """Update given hash object (using hash_object.update()) such that it changes
        whenever the environment specified via self.spec could potentially contain a
        different set of software (in terms of versions or packages).
        """
        ...

    @abstractmethod
    def report_software(self) -> Iterable[SoftwareReport]:
        """Report the software contained in the environment. This should be a list of
        snakemake_interface_software_deployment_plugins.SoftwareReport data class.
        Use SoftwareReport.is_secondary = True if the software is just some
        less important technical dependency. This allows Snakemake's report to
        hide those for clarity. In case of containers, it is also valid to
        return the container URI as a "software".
        Return an empty tuple () if no software can be reported.
        """
        ...

    def run_cmd(self, cmd: str, **kwargs) -> sp.CompletedProcess:
        """Run a command while potentially respecting the self.within environment,
        returning the result of subprocess.run.

        kwargs is passed to subprocess.run, shell=True is always set.
        """
        if self.within is not None:
            cmd = self.within.managed_decorate_shellcmd(cmd)
        return sp.run(cmd, shell=True, executable=self.shell_executable, **kwargs)

    def managed_decorate_shellcmd(self, cmd: str) -> str:
        cmd = self.decorate_shellcmd(cmd)
        if self.within is not None:
            cmd = self.within.managed_decorate_shellcmd(cmd)
        return cmd

    def hash(self) -> str:
        return self._managed_generic_hash("hash")

    def _managed_generic_hash(self, kind: str) -> str:
        store = getattr(self, f"_managed_{kind}_store")
        if store is None:
            record_hash = f"record_{kind}"
            hash_object = hashlib.md5()
            if self.within is not None:
                getattr(self.within, record_hash)(hash_object)
            getattr(self, record_hash)(hash_object)
            store = hash_object.hexdigest()
        return store

    def __hash__(self) -> int:
        # take the hash of all fields by settings, _managed_hash_store and _managed_deployment_hash_store
        if self._obj_hash is None:
            self._obj_hash = hash(self.hash())
        return self._obj_hash

    def __eq__(self, other) -> bool:
        return (
            self.__class__ == other.__class__
            and self.spec == other.spec
            and self.hash() == other.hash()
        )


class DeployableEnvBase(ABC):
    @abstractmethod
    def is_deployment_path_portable(self) -> bool: ...

    @abstractmethod
    async def deploy(self) -> None:
        """Deploy the environment to self.deployment_path.

        When issuing shell commands, the environment should use
        self.run_cmd(cmd: str) in order to ensure that it runs within eventual
        parent environments (e.g. a container or an env module).
        """
        ...

    def record_deployment_hash(self, hash_object) -> None:
        """Update given hash such that it changes whenever the environment
        needs to be redeployed, e.g. because its content has changed or the
        deployment location has changed. The latter is only relevant if the
        deployment is senstivive to the path (e.g. in case of conda, which patches
        the RPATH in binaries).
        """
        self.record_hash(hash_object)
        if not self.is_deployment_path_portable():
            hash_object.update(str(self._deployment_prefix).encode())

    @abstractmethod
    def remove(self) -> None:
        """Remove the deployed environment."""
        ...

    def managed_deploy(self) -> None:
        if isinstance(self, ArchiveableEnvBase) and self.archive_path.exists():
            self.deploy_from_archive()
        else:
            self.deploy()

    def deployment_hash(self) -> str:
        return self._managed_generic_hash("deployment_hash")

    @property
    def deployment_path(self) -> Path:
        return self._deployment_prefix / self.deployment_hash()


class ArchiveableEnvBase(ABC):
    @abstractmethod
    async def archive(self) -> None:
        """Archive the environment to self.archive_path.

        When issuing shell commands, the environment should use
        self.run_cmd(cmd: str) in order to ensure that it runs within eventual
        parent environments (e.g. a container or an env module).
        """
        ...

    @property
    def archive_path(self) -> Path:
        return self._archive_prefix / self.hash()
