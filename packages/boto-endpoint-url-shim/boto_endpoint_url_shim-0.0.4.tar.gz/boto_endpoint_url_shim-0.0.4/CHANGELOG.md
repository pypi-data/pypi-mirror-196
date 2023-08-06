# Changelog

All notable changes to this project will be documented in this file.

Unless otherwise stated, these changes have been implemented by [ljmc][ljmc].

This project adheres to [Semantic Versioning][semver].

The format is based on [Keep a Changelog][changelog].

[ljmc]: https://gitlab.com/ljmc
[semver]: https://semver.org/spec/v2.0.0.html
[changelog]: https://keepachangelog.com/en/1.1.0/

## unreleased

## v0.0.4 (2023-03-11)

### Added

* `IGNORE_ENV_VAR` and `IGNORE_PARAM` constants for ignoring custom endpoint URL
* tests for ignoring custom endpoint URL:
    * `test_custom_endpoint_url_resolution_disabled_by_env_var`
    * `test_custom_endpoint_url_resolution_disabled_config_file`
    * `test_custom_endpoint_url_resolution_disabled_kwarg`
* `test_read_mapping_env_var_already_loaded` to cover `read_mapping_env_var`
  with already cached map

### Changed

* added `ignore_config_endpoint_urls` keyword argument to `create_client` method
* added `ignore_config_endpoint_urls` argument to `_resolve_endpoint_url` method
* `_resolve_endpoint_url` checks `ignore_config_endpoint_urls` argument, env var
  `IGNORE_ENV_VAR` and `IGNORE_PARAM` from shared config profile to ignore
  custom endpoint
* renamed `test_read_mapping_env_var` to `test_read_mapping_env_var_not_loaded`

## v0.0.3 (2023-03-11)

### Fixed

* Environment variables format changed to match update

## v0.0.2 (2023-03-01)

### Added

* Add `_custom_build_profile_map` for services sections in shared configuration
  file
* Tests for services sections

### Changed

* `proposed_endpoint_url_resolution` now includes global resolution options
* `_patch_botocore`/`_unpatch_botocore` patches/unpatched
  `botocore.session.Session` and `botocore.configloader.build_profile_map`
* Rename `ORIGINAL_BOTOCORE_SESSION` to `BOTOCORE_PATCHED` and store both
  original `Session` and `build_profile_map`

### Removed

* Remove `global_endpoint_url_resolution`

## v0.0.1 (2022-12-18)

### Added

* First release
* Pushed to `pypi`
