__author__ = "Johannes Köster"
__copyright__ = "Copyright 2024, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod
from copy import copy
from inspect import getmodule
from dataclasses import dataclass, field
import hashlib
from pathlib import Path
import shutil
from types import ModuleType
from typing import (
    Any,
    ClassVar,
    Dict,
    Iterable,
    List,
    Optional,
    Self,
    Tuple,
    Type,
    Union,
    Callable,
)
import subprocess as sp

from snakemake_interface_common.exceptions import WorkflowError


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
    @classmethod
    def module(cls) -> ModuleType:
        class_module = getmodule(cls)
        assert class_module is not None, f"bug: cannot detect class module of {cls}"
        return class_module

    def technical_init(self):
        """This has to be called by Snakemake upon initialization"""
        self.within: Optional["EnvSpecBase"] = None
        self.fallback: Optional["EnvSpecBase"] = None
        self.kind: str = self.module().common_settings.provides
        self._obj_hash: Optional[int] = None

    @classmethod
    def env_cls(cls) -> Type["EnvBase"]:
        try:
            return cls.module().EnvBase
        except AttributeError:
            raise AttributeError(
                "No class Env found next to EnvSpec class. "
                "Make sure to import or define it there."
            )

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

    def modify_source_paths(self, modify_func: Callable) -> Self:
        return self._modify_attributes("source_path_attributes", modify_func)

    def modify_identity_attributes(self, modify_func: Callable) -> Self:
        return self._modify_attributes("identity_attributes", modify_func)

    def _modify_attributes(self, attribute_method: str, modify_func: Callable) -> Self:
        if self.has_source_paths():
            self_or_copied = copy(self)
        else:
            return self
        for attr_name in getattr(self_or_copied, attribute_method):
            current_value = getattr(self_or_copied, attr_name)
            if current_value is not None:
                setattr(self_or_copied, attr_name, modify_func(current_value))

        if self_or_copied.within is not None:
            self_or_copied.within = self_or_copied.within._modify_attributes(
                attribute_method,
                modify_func,
            )

        if self_or_copied.fallback is not None:
            self_or_copied.fallback = self_or_copied.fallback._modify_attributes(
                attribute_method,
                modify_func,
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

    @abstractmethod
    def __str__(self) -> str:
        """Return a string representation of the environment spec."""
        ...


@dataclass
class ShellExecutable:
    executable: str
    command_arg: str
    args: List[str] = field(default_factory=list)

    @property
    def name(self) -> str:
        return Path(self.executable).name

    def run(self, cmd: str, **kwargs) -> sp.CompletedProcess:
        return sp.run([self.executable] + self.args + [self.command_arg, cmd], **kwargs)


class EnvBase(ABC):
    _cache: ClassVar[Dict[Tuple[Type["EnvBase"], Optional["EnvBase"]], Any]] = {}

    def __init__(
        self,
        spec,
        within: Optional["EnvBase"],
        settings,
        shell_executable: ShellExecutable,
        mountpoints: List[Path],
        tempdir: Path,
        cache_prefix: Path,
        deployment_prefix: Path,
        pinfile_prefix: Path,
    ):
        # type annotation for spec and settings is left for implementing plugins
        self.spec = spec
        self.within = within
        self.settings = settings
        self.shell_executable = shell_executable
        self.mountpoints = mountpoints
        self.tempdir = tempdir
        self._deployment_prefix: Path = deployment_prefix
        self._cache_prefix: Path = cache_prefix
        self._pinfile_prefix: Path = pinfile_prefix
        self._managed_hash_store: Optional[str] = None
        self._managed_deployment_hash_store: Optional[str] = None
        self._obj_hash: Optional[int] = None
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
    def contains_executable(self, executable: str) -> bool:
        ...

    def is_deployable(self) -> bool:
        """Overwrite this in case the deployability of the environment depends on
        the spec or settings."""
        return isinstance(self, DeployableEnvBase)

    def is_pinnable(self) -> bool:
        """Overwrite this in case the pinability of the environment depends on
        the spec or settings."""
        return isinstance(self, PinnableEnvBase)

    def is_cacheable(self) -> bool:
        """Overwrite this in case the cacheability of the environment depends on
        the spec or settings."""
        return isinstance(self, CacheableEnvBase)

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
        assert "shell" not in kwargs, "shell argument has to be set to False"
        if self.within is not None:
            cmd = self.within.managed_decorate_shellcmd(cmd)
        return self.shell_executable.run(cmd, **kwargs)

    def managed_decorate_shellcmd(self, cmd: str) -> str:
        cmd = self.decorate_shellcmd(cmd)
        if self.within is not None:
            cmd = self.within.managed_decorate_shellcmd(cmd)
        return cmd

    def hash(self) -> str:
        return self._managed_generic_hash("hash")

    def _managed_generic_hash(self, kind: str) -> str:
        store_attr = f"_managed_{kind}_store"
        store = getattr(self, store_attr)
        if store is None:
            record_hash = f"record_{kind}"
            hash_object = hashlib.md5()
            if self.within is not None:
                # For within, we always take the normal hash,
                # since the deployment just runs within that.
                self.within.record_hash(hash_object)
            getattr(self, record_hash)(hash_object)
            store = hash_object.hexdigest()
            setattr(self, store_attr, store)
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


class PinnableEnvBase(EnvBase, ABC):
    @classmethod
    @abstractmethod
    def pinfile_extension(cls) -> str: ...

    @abstractmethod
    async def pin(self) -> None:
        """Pin the environment to potentially more concrete versions than defined.
        Only implement this base class if pinning makes sense for your kind of
        environment. Pinfile has to be written to self.pinfile.
        """
        ...

    @property
    def pinfile(self) -> Path:
        ext = self.pinfile_extension()
        if not ext.startswith("."):
            raise ValueError("pinfile_extension must start with a dot.")
        return (self._pinfile_prefix / self.hash()).with_suffix(
            self.pinfile_extension()
        )

    def remove_pinfile(self) -> None:
        """Remove the pinfile."""
        if self.pinfile.exists():
            try:
                self.pinfile.unlink()
            except Exception as e:
                raise WorkflowError(
                    f"Removal of pinfile {self.pinfile} failed: {e}"
                ) from e


class CacheableEnvBase(EnvBase, ABC):
    async def get_cache_assets(self) -> Iterable[str]: ...

    @abstractmethod
    async def cache_assets(self) -> None:
        """Determine environment assets and store any associated information or data to
        self.cache_path.
        """
        ...

    @property
    def cache_path(self) -> Path:
        return self._cache_prefix

    async def remove_cache(self) -> None:
        """Remove the cached environment assets."""
        for asset in await self.get_cache_assets():
            asset_path = self.cache_path / asset
            if asset_path.exists():
                try:
                    if asset_path.is_dir():
                        shutil.rmtree(asset_path)
                    else:
                        asset_path.unlink()
                except Exception as e:
                    raise WorkflowError(
                        f"Removal of cache asset {asset_path} for {self.spec} failed: {e}"
                    ) from e


class DeployableEnvBase(EnvBase, ABC):
    @abstractmethod
    def is_deployment_path_portable(self) -> bool:
        """Return whether the deployment path matters for the environment, i.e.
        whether the environment is portable. If this returns False, the deployment
        path is considered for the deployment hash. For example, conda environments are not
        portable because they hardcode the path in binaries, while containers are
        portable.
        """
        ...

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

    def managed_remove(self) -> None:
        """Remove the deployed environment, handling exceptions."""
        try:
            self.remove()
        except Exception as e:
            raise WorkflowError(f"Removal of {self.spec} failed: {e}") from e

    async def managed_deploy(self) -> None:
        try:
            await self.deploy()
        except Exception as e:
            raise WorkflowError(f"Deployment of {self.spec} failed: {e}") from e

    def deployment_hash(self) -> str:
        return self._managed_generic_hash("deployment_hash")

    @property
    def deployment_path(self) -> Path:
        assert self._deployment_prefix is not None
        return self._deployment_prefix / self.deployment_hash()
