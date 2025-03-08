from abc import ABC, abstractmethod
import asyncio
from copy import deepcopy
from typing import Optional, Type
import subprocess as sp

import pytest

from snakemake_interface_software_deployment_plugins import (
    ArchiveableEnvBase,
    DeployableEnvBase,
    EnvBase,
    EnvSpecBase,
    EnvSpecSourceFile,
    SoftwareReport,
)
from snakemake_interface_software_deployment_plugins.settings import (
    SoftwareDeploymentSettingsBase,
)


_TEST_SDM_NAME = "test-sdm"


class TestSoftwareDeploymentBase(ABC):
    __test__ = False
    shell_executable = "bash"

    @abstractmethod
    def get_env_spec(self) -> EnvSpecBase:
        """
        If the software deployment provider does not support deployable environments,
        this method should return args for an existing environment spec that can be used
        for testing
        """
        ...

    @abstractmethod
    def get_env_cls(self) -> Type[EnvBase]:
        """
        Return the environment class that should be tested.
        """
        ...

    @abstractmethod
    def get_test_cmd(self) -> str:
        """
        Return a test command that should be executed within the environment
        with exit code 0 (i.e. without error).
        """
        ...

    @abstractmethod
    def get_software_deployment_provider_settings(
        self,
    ) -> Optional[SoftwareDeploymentSettingsBase]: ...

    def test_shellcmd(self, tmp_path):
        env = self._get_env(tmp_path)

        if isinstance(env, DeployableEnvBase):
            pytest.skip("Environment is deployable, using test_deploy instead.")

        cmd = self.get_test_cmd()
        decorated_cmd = env.managed_decorate_shellcmd(cmd)
        assert cmd != decorated_cmd
        assert (
            sp.run(
                decorated_cmd, shell=True, executable=self.shell_executable
            ).returncode
            == 0
        )

    def test_deploy(self, tmp_path):
        env = self._get_env(tmp_path)
        self._deploy(env, tmp_path)
        cmd = env.managed_decorate_shellcmd(self.get_test_cmd())
        assert sp.run(cmd, shell=True, executable=self.shell_executable).returncode == 0

    def test_archive(self, tmp_path):
        env = self._get_env(tmp_path)
        if not isinstance(env, ArchiveableEnvBase):
            pytest.skip("Environment either not deployable or not archiveable.")

        self._deploy(env, tmp_path)

        asyncio.run(env.archive())
        assert any((tmp_path / "archives").iterdir())

    def test_report_software(self, tmp_path):
        env = self._get_env(tmp_path)
        rep = env.report_software()
        assert all(isinstance(s, SoftwareReport) for s in rep)

    def test_identity_attributes(self):
        spec = self.get_env_spec()
        assert all(
            isinstance(attr, str) and hasattr(spec, attr)
            for attr in spec.identity_attributes()
        )

    def test_source_path_attributes(self):
        spec = self.get_env_spec()
        assert all(
            isinstance(attr, str)
            and hasattr(spec, attr)
            and isinstance(getattr(spec, attr), (EnvSpecSourceFile, None))
            for attr in spec.source_path_attributes()
        ), "bug in plugin: all source path attributes must be of type EnvSpecSourceFile"

    def _get_cached_env_spec(self):
        spec = deepcopy(self.get_env_spec())
        for attr in spec.source_path_attributes():
            source_file = getattr(spec, attr)
            source_file.cached = source_file.path_or_uri
        return spec

    def _get_env(self, tmp_path) -> EnvBase:
        env_cls = self.get_env_cls()
        spec = self._get_cached_env_spec()
        args = {"settings": self.get_software_deployment_provider_settings()}
        if issubclass(env_cls, DeployableEnvBase):
            args["deployment_prefix"] = tmp_path / "deployments"
        if issubclass(env_cls, ArchiveableEnvBase):
            args["archive_prefix"] = tmp_path / "archives"
        return env_cls(
            spec=spec, within=None, shell_executable=self.shell_executable, **args
        )

    def _deploy(self, env: DeployableEnvBase, tmp_path):
        if not isinstance(env, DeployableEnvBase):
            pytest.skip("Environment is not deployable.")

        asyncio.run(env.deploy())
        assert any((tmp_path / "deployments").iterdir())
