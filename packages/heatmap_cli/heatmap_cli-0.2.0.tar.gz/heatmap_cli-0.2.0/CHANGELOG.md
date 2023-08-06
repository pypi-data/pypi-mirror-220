# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [0-based versioning](https://0ver.org/).

## [Unreleased]

## v0.2.0 (2023-07-23)

## Added

- Add `yr` or `--year` argument to filter CSV data by year
- Add `wk` or `--week` argument to filter CSV data until week of the year
- Add additional pre-commit default checks
- Show generated PNG filename upon completion

### Changed

- Group all `sphinx` related deps under the `doc` category
- Standardize `tox` environment names

### Fixed

- Fix incorrect ignored coverage module
- Suppress logging from `matplotlib` in `debug` mode

## v0.1.3 (2023-07-16)

### Fixed

- Fix missing `pylint` dependency when running `pre-commit`
- Ignore word when running `codespell` pre-commit hook

## v0.1.2 (2023-07-11)

### Changed

- Link to license from contributing doc
- Use the same output folder for `sphinx` doc generation
- Revise `pyenv` installation with plugins in contributing doc
- Install `heatmap_cli` as editable installation in `pipenv` dev env

## v0.1.1 (2023-07-09)

### Fixed

- Fix missing dependencies on `pipx` installation
- Fix incorrect module name in `pre-commit` hooks

## v0.1.0 (2023-07-08)

### Added

- Initial public release
