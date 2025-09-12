# Changelog

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
