<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# Changelog

All notable changes to the trivval project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.2] - 2023-03-10

### Fixes

- Do not refer to `stubs/` in the manifest file, that directory is gone.
- Lots of minor refactoring suggested by the Ruff tool.
- Fix the Markdown syntax for nested lists in the changelog file.

### Additions

- Add Tox environment tags for the `tox-stages` tool.
- Add the `nix/python-pytest.nix` expression to run `pytes` with
  the specified Python version.
- Add the `nix/run-pytest.sh` tool to run `nix/python-pytest.nix` with
  all the currently supported Python versions.
- Add the `reuse` and `pyupgrade` Tox test environments that are only
  ever supposed to be invoked manually, followed by a careful check.
- Add the `ruff` and `ruff-all` test environments to run the Ruff static
  code analyzer.

### Other changes

- Pass information about supported Python versions to the `pylint` and
  `black` tools.
- Switch to SPDX license tags.
- Drop the Markdown file format unit test; the changelog file is now in
  the "Keep a Changelog" format and may be validated using other tools.
- Use deferred annotations in all the Python source files, just in case.
- Use `black-23.x`, `flake8-6.x`, `mypy-1.x`, and `pylint-2.16.x` with
  no changes to the source code
- Mention `ruff`, `tox-changes`, and `python-pytest.nix` in
  the `HACKING.md` development guide.
- Reformat the changelog file to follow the "Keep a Changelog" style:
      - turn the entry version strings into "list the commits since
        the previous version" hyperlinks
      - organize the entries into internal sections
      - add a blurb at the top
      - add an "Unreleased" entry at the top

## [1.1.1] - 2022-09-14

### Semi-incompatible changes

- Drop support for Python 3.6:
    - the dataclasses module is fully available now
    - use deferred type annotations
    - use native collection types (dict, list, tuple) instead of
      the typing library generics
    - use the X | Y syntax for unions

### Fixes

- Silence a pylint test positive in a unit test.
- Fix a bug in constructing an error message.

### Additions

- List Python 3.10 and 3.11 as supported versions.
- Add a very much incomplete HACKING.md style and development guide.
- Add a tox.nix expression for running Tox using the Nix shell.

### Other changes

- Reformat the source code with 100 characters per line.
- Tox test refactoring and improvements:
    - drop the flake8 + hacking test environment
    - drop the useless "basepython = python3" lines
    - use a multiline list for defs.pyfiles
    - add lower and upper version constraints to all the modules that
      the test environments depend on
    - drop the pytest.pyi typing stub and install pytest 7.x in
      the mypy test environment; it has type annotations now

## [1.1.0] - 2021-04-07

### Additions

- Allow an optional key to be present with a null value.

## [1.0.2] - 2021-03-31

### Additions

- Add Python 3.9 as a supported version.
- Add a PEP 517 build framework.
- Add a manifest file for the source distribution.

### Other changes

- Drop the outdated pylintrc file.
- Move some tool configuration options to setup.py and pyproject.toml.
- Rename some of the tox environments.
- Push the source down into a src/ directory.
- Drop the unit-tests-bare tox environment.
- Add a mypy stub file for pytest.
- Go back to using packaging instead of the deprecated distutils.

## [1.0.1] - 2020-09-06

### Fixes

- Propagate a ValidationError's traceback information when
  reraising it in an outer scope.

### Other changes

- Reformat the source code using black 20.
- Use distutils.version instead of packaging.version.
- Use super() with no arguments we depend on Python 3.x.

## [1.0.0] - 2020-04-14

### Incompatible changes

- Only support Python 3.6 or later:
    - drop the Python 2.x unit tests and mypy check
    - unconditionally import typing and pathlib
    - drop the "equivalent types" support only needed for
      the Python 2.x `unicode`/`str` weirdness
    - no longer inherit from `object`
    - use f-strings for errors and diagnostic messages
    - use Python 3.x's `unittest.mock` and drop `fake_mock`

### Other changes

- Use the `mistune` library to validate the Markdown files.

## [0.1.0] - 2020-04-14

### Started

- First public release.

[Unreleased]: https://gitlab.com/ppentchev/python-trivval/-/compare/release%2F1.1.2...master
[1.1.2]: https://gitlab.com/ppentchev/python-trivval/-/compare/release%2F1.1.1...release%2F1.1.2
[1.1.1]: https://gitlab.com/ppentchev/python-trivval/-/compare/release%2F1.1.0...release%2F1.1.1
[1.1.0]: https://gitlab.com/ppentchev/python-trivval/-/compare/release%2F1.0.2...release%2F1.1.0
[1.0.2]: https://gitlab.com/ppentchev/python-trivval/-/compare/release%2F1.0.1...release%2F1.0.2
[1.0.1]: https://gitlab.com/ppentchev/python-trivval/-/compare/release%2F1.0.0...release%2F1.0.1
[1.0.0]: https://gitlab.com/ppentchev/python-trivval/-/compare/release%2F0.1.1...release%2F1.0.0
[0.1.1]: https://gitlab.com/ppentchev/python-trivval/-/compare/release%2F0.1.0...release%2F0.1.1
[0.1.0]: https://gitlab.com/ppentchev/python-trivval/-/tags/release%2F0.1.0
