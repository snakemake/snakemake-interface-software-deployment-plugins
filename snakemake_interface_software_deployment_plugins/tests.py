from abc import ABC, abstractmethod
from typing import Optional
import subprocess as sp

import pytest

from snakemake_interface_software_deployment_plugins import ArchiveableEnvBase, DeployableEnvBase, EnvBase, EnvSpecBase, SoftwareDeploymentProviderBase
from snakemake_interface_software_deployment_plugins.settings import SoftwareDeploymentProviderSettingsBase


_TEST_SDM_NAME = "test-sdm"



class TestStorageBase(ABC):
    __test__ = False

    @abstractmethod
    def get_software_deployment_provider_class(self) -> SoftwareDeploymentProviderBase:
        ...

    @abstractmethod
    def get_env_spec(self) -> EnvSpecBase:
        """
        If the software deployment provider does not support deployable environments,
        this method should return an existing environment spec that can be used for
        testing
        """
        ...

    @abstractmethod
    def get_test_cmd(self) -> str:
        """
        Return a test command that should be executed within the environment
        with exit code 0 (i.e. without error).
        """
        ...

    def get_software_deployment_provider_settings(self) -> Optional[SoftwareDeploymentProviderSettingsBase]:
        return None

    def test_shellcmd(self, tmp_path):
        provider = self._get_provider(tmp_path)
        env = self._get_env(provider)

        if isinstance(env, DeployableEnvBase):
            pytest.skip("Environment is deployable, using test_deploy instead.")

        cmd = self.get_test_cmd()
        decorated_cmd = env.managed_decorate_shellcmd(cmd)
        assert cmd != decorated_cmd
        assert sp.run(decorated_cmd, shell=True).returncode == 0

    def test_deploy(self, tmp_path):
        provider = self._get_provider(tmp_path)
        env = self._get_env(provider)
        self._deploy(env, tmp_path)
        cmd = env.managed_decorate_shellcmd(self.get_test_cmd())
        assert sp.run(cmd, shell=True).returncode == 0

    def test_archive(self, tmp_path):
        provider = self._get_provider(tmp_path)
        env = self._get_env(provider)
        if not isinstance(env, ArchiveableEnvBase):
            pytest.skip("Environment either not deployable or not archiveable.")

        self._deploy(env, tmp_path)

        env.archive()
        assert any((tmp_path / "{_TEST_SDM_NAME}-archive").iterdir())

    def _get_env(self, provider) -> EnvBase:
        return provider.get_env(spec=self.get_env_spec())

    def _deploy(self, env: DeployableEnvBase, tmp_path):
        if not isinstance(env, DeployableEnvBase):
            pytest.skip("Environment is not deployable.")

        env.deploy()
        assert any((tmp_path / _TEST_SDM_NAME).iterdir())

    def _get_provider(self, tmp_path):
        return self.get_software_deployment_provider_class()(
            name=_TEST_SDM_NAME,
            prefix=tmp_path,
            settings=self.get_software_deployment_provider_settings(),
            parent_env=None, # TODO also test with parent env once we have determined how this will work
        )

