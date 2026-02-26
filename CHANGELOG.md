# Changelog

## [0.12.0](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.11.0...v0.12.0) (2026-02-26)


### Features

* make env spec generic ([c7b9971](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/c7b9971d779909081e50b45ff5f858e67435bd08))


### Bug Fixes

* make generic args more flexible ([af21397](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/af21397717e9400c5a335f3fde5950b9f522626c))
* relax typing ([0f10324](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/0f10324da494b2fe4b46616aa283abd7f96dcc09))
* simplify mountpoint information into self.mountpoints, complemented by self.tempdir holding the temporary directory to use ([7112ee6](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/7112ee6bb5eed944dab7da90a30255431b0042bd))

## [0.11.0](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.10.2...v0.11.0) (2026-02-23)


### Features

* make EnvBase generic; enable EnvSpecBase recursive attribute modification ([1425a51](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/1425a516a5c7152bdb6e291d602247ab8e0b4412))

## [0.10.2](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.10.1...v0.10.2) (2026-02-18)


### Bug Fixes

* allow missing args argument for shell executable ([d7bca35](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/d7bca35b5f27058d3ef1011283b3752373970bef))

## [0.10.1](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.10.0...v0.10.1) (2026-02-17)


### Bug Fixes

* deployments path in test suite ([971dea2](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/971dea2f0d0ad330765b7eccb7e2eaee056aa715))
* hash building for enclosed environments and deployment test ([#38](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/issues/38)) ([89d45d8](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/89d45d8a665639848dd2e1a76f2e5b9a6ea2ff06))
* unique deployment path ([d953afe](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/d953afe4732b356d1b0f27469d4a3aaad56159b4))

## [0.10.0](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.9.1...v0.10.0) (2026-02-13)


### Features

* add get_within() method to TestSoftwareDeploymentBase ([1f990f1](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/1f990f12b77b61f2a6f64a974b1c4b3819864196))

## [0.9.1](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.9.0...v0.9.1) (2026-02-13)


### Bug Fixes

* typing, add pyrefly, migrate to pixi ([#34](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/issues/34)) ([6532631](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/65326312670f2865d1433c7d71fb3ce32366fc9b))

## [0.9.0](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.8.0...v0.9.0) (2025-10-01)


### Features

* add source cache path attribute for mounting in e.g. containers ([#33](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/issues/33)) ([7962913](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/796291391c670bb528327383799035d48cf06877))
* allow removal of pinfile ([#31](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/issues/31)) ([8e453b2](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/8e453b242f1a2268daa160730099647adb9f9a5b))

## [0.8.0](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.7.7...v0.8.0) (2025-09-19)


### Features

* use class for representing shell executable ([fd3e9f9](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/fd3e9f9e1ac66a194046f38558e4d6bd880b1dd2))

## [0.7.7](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.7.6...v0.7.7) (2025-09-19)


### Bug Fixes

* use EnvBase.run_cmd in test suite ([e46ee97](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/e46ee9785d1c105341834a416b526d684d52f5c4))

## [0.7.6](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.7.5...v0.7.6) (2025-09-19)


### Bug Fixes

* use login shell by default ([d7fcf57](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/d7fcf57ae4e6a4fe7fe145df19e8a28ec6960e6b))

## [0.7.5](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.7.4...v0.7.5) (2025-09-15)


### Bug Fixes

* use method for testing if env is deployable in test suite ([1c64a8f](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/1c64a8f96554133ed1150ab00a55303dac1e68cc))

## [0.7.4](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.7.3...v0.7.4) (2025-09-12)


### Bug Fixes

* properly check source file type in test suite ([#25](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/issues/25)) ([b0df467](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/b0df4670ff8ab8097cf5c281ab3f13859c718ae9))

## [0.7.3](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.7.2...v0.7.3) (2025-09-12)


### Bug Fixes

* use Protocol type ([#23](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/issues/23)) ([2a10a4a](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/2a10a4a011515de79dd1c7eff0a8bfc6a8217416))

## [0.7.2](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.7.1...v0.7.2) (2025-09-12)


### Bug Fixes

* handle None type for source file attributes in EnvSpec ([#21](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/issues/21)) ([247d066](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/247d06669854b06b38c58b3e9c023fd45e765391))

## [0.7.1](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.7.0...v0.7.1) (2025-09-12)


### Bug Fixes

* adapt tests to API changes ([#19](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/issues/19)) ([3f37e5f](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/3f37e5faf50869fcf18a33e1b1ae7feb382cb9d6))

## [0.7.0](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.6.1...v0.7.0) (2025-09-11)


### Features

* deploy from archive ([#18](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/issues/18)) ([f6d62bd](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/f6d62bd6530673c6fbbad382807378dbdcbf0023))
* pass tempdir to EnvBase ([#16](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/issues/16)) ([28d8351](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/28d83516691e1e90edb00d17bb44d437c69a332d))

## [0.6.1](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.6.0...v0.6.1) (2025-03-08)


### Bug Fixes

* change methods into classmethods ([358695c](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/358695ce97f036b5e44d0ce6f0a15c7c9cce832f))
* remove deploy_from_archive ([8831501](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/8831501a1ec3286bd7342ab34a523f3944bc2153))

## [0.6.0](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.5.0...v0.6.0) (2025-03-07)


### Features

* introduce EnvSpecSourceFile as a container data class for paths or uris mentioned in the EnvSpec that shall be cached and resolved by Snakemake's source caching mechanism ([#13](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/issues/13)) ([d359609](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/d359609bf2dd01a1b29814c76eb7276d657c2b27))

## [0.5.0](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.4.0...v0.5.0) (2025-03-07)


### Features

* make deploy async ([#11](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/issues/11)) ([217b965](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/217b965e8c07f1ae05aa8657c8914b8efdc6c073))

## [0.4.0](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.3.0...v0.4.0) (2025-03-07)


### Features

* add abstract method for reporting software ([#9](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/issues/9)) ([f7b6d6c](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/f7b6d6c190be74cc0e036f3c02d8cdee79abdfb4))

## [0.3.0](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.2.3...v0.3.0) (2025-03-06)


### Features

* add method to modify source paths in EnvSpecBase ([d946bb4](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/d946bb4534e09ebba25c385cd8b599736492e0c1))
* Env and EnvSpec comparison and hashing ([37c334f](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/37c334f6080b5ca907d6a3e05225d2f48239df71))
* introduce common settings ([8de4dec](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/8de4dec75f654eba05f7916e442c107253393069))


### Bug Fixes

* check provides validity ([8b39604](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/8b39604f5d77070b909819af6e1b5af7f21980dc))
* test suite abstract method ([9d278f9](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/9d278f928fb40aaf4090359af2d8f84d22391a74))

## [0.2.3](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.2.2...v0.2.3) (2025-03-06)


### Bug Fixes

* expose shell executable setting ([ca35ce5](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/ca35ce5656a6086b3f4ff1c188fb4b6d1cc77163))

## [0.2.2](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.2.1...v0.2.2) (2025-03-06)


### Bug Fixes

* fix EnvBase.once decorator ([ea468eb](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/ea468eb37f79ff177a37d2077d9c9e171a832945))

## [0.2.1](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.2.0...v0.2.1) (2025-03-06)


### Bug Fixes

* fix function args of once decorator ([74dde47](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/74dde475b81cc1f9d5bd34ed9a714f6782fc0263))

## [0.2.0](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.1.1...v0.2.0) (2025-03-06)


### Features

* cache decorator and "or"/fallback support for EnvSpecBase ([ee465b0](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/ee465b05dafe85d459ba3d16dbb51311663deb5c))

## [0.1.1](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/compare/v0.1.0...v0.1.1) (2025-03-05)


### Bug Fixes

* run test cmd in bash ([85effcf](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/85effcf86792f474fcfb0f880c36694e5dfe2307))

## 0.1.0 (2025-03-05)


### Miscellaneous Chores

* release 0.1.0 ([3dd0101](https://github.com/snakemake/snakemake-interface-software-deployment-plugins/commit/3dd0101b3b20c6b5f4e89cc889475e09eb12d050))
