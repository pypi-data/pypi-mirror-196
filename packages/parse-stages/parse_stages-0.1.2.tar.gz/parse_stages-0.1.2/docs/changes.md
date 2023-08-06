<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# Changelog

All notable changes to the parse-stages project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2023-03-10

### Semi-incompatible changes

- Drop Python 3.7 support.

### Fixes

- Fix the 0.1.1 release URL in the changelog file.
- Do not run the `pyupgrade` Tox environment automatically.
- Add a docstring to the unit test suite's `__init__.py` file instead of
  overriding a linter check.

### Additions

- Start some MkDocs-based documentation.
- Add the `reuse` Tox test environment to run the REUSE tool manually.

### Other changes

- Rework the Ruff invocation Tox targets a bit:
    - drop the `ruff-all-unchained` test environment; at this point in
      Ruff's development we are bound to specific versions anyway
    - move the config files to a `config/` directory, not `.config/`
    - move the "normal" Ruff invocation configuration to `config/ruff-most/`
    - use Ruff 0.0.254 with no code changes
    - activate all of Ruff 0.0.254's liners in the "normal" invocation
- Switch to SPDX license tags.
- Specify the supported Python version in the configuration of the pylint and
  black tools.
- Move the changelog file into the documentation directory.
- In the packaging metadata, point to the Ringlet homepage generated from
  the newly-added documentation.

## [0.1.1] - 2023-02-05

### Fixes

- Use "precedence" instead of "priority" when discussing operators in
  the README file.
- Do not use the `list` generic type in the definition of the `TaggedFrozen` and
  `Tagged` classes; library consumers may try to use `typing.get_type_hints()` on
  them or on derived classes, and Python < 3.9 would have a problem with that.
- Fill in the module docstring using the text of the README file.
- Fix some problems reported by `ruff`:
    - fix the order of some `import` statements
    - fix the formatting of some docstrings

### Other changes

- Add the `ruff-all` test environment that enables all the checks of the `ruff`
  tool for a certain locked version of `ruff`.
- Add the `tool.test-stages` section in the `pyproject.toml` file to specify
  the order that Tox environments should be run during development using
  the `tox-stages` tool from the `test-stages` Python library.
- Add a lot of `flake8` plugins to the Tox `pep8` test environment
- Use ruff 0.0.241, pylint 2.16.x, and black 23.x.

## [0.1.0] - 2023-01-25

### Started

- First public release.

[Unreleased]: https://gitlab.com/ppentchev/parse-stages/-/compare/release%2F0.1.2...main
[0.1.2]: https://gitlab.com/ppentchev/parse-stages/-/compare/release%2F0.1.1...release%2F0.1.2
[0.1.1]: https://gitlab.com/ppentchev/parse-stages/-/compare/release%2F0.1.0...release%2F0.1.1
[0.1.0]: https://gitlab.com/ppentchev/parse-stages/-/tags/release%2F0.1.0
