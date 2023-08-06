# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Simple tests for the validation routine."""

from __future__ import annotations

import json

from unittest import mock

from typing import Any

import pytest

import trivval

from . import data as tdata


def do_test(value: dict[str, Any], schema: dict[str, Any], *, backwards: bool = False) -> None:
    """Run the tests for a specific value against a schema."""

    def test_extra_succeed() -> None:
        trivval.validate_dict(value, schema, 0)

    def test_extra_fail() -> None:
        with pytest.raises(trivval.ValidationError) as err:
            trivval.validate_dict(value, schema, 0)
        assert err.value.path[-1] != "a,more"
        assert err.value.err.startswith("extra")

    test_extra = test_extra_fail if backwards else test_extra_succeed

    trivval.validate_dict(value, schema, trivval.FLAG_ALLOW_EXTRA)
    test_extra()

    if "node" in value:
        add_to = value["node"]
        add_path = ["node"]
    else:
        add_key = next(iter(value["nodes"].keys()))
        add_to = value["nodes"][add_key]
        add_path = ["nodes", add_key]
    assert "more" not in add_to and "a" not in add_to
    add_to.update({"a": "lot", "more": "stuff"})
    trivval.validate_dict(value, schema, trivval.FLAG_ALLOW_EXTRA)
    with pytest.raises(trivval.ValidationError) as err:
        trivval.validate_dict(value, schema, 0)
    if not backwards:
        assert err.value.path == [*add_path, "a,more"]
        assert err.value.err.startswith("extra")

    del add_to["a"]
    del add_to["more"]
    trivval.validate_dict(value, schema, trivval.FLAG_ALLOW_EXTRA)
    test_extra()

    missing = add_to.pop("hostname")

    with pytest.raises(trivval.ValidationError) as err:
        trivval.validate_dict(value, schema, trivval.FLAG_ALLOW_EXTRA)
    assert err.value.path == [*add_path, "hostname"]
    assert err.value.err.startswith("missing")

    with pytest.raises(trivval.ValidationError) as err:
        trivval.validate_dict(value, schema, 0)
    if not backwards:
        assert err.value.path == [*add_path, "hostname"]
        assert err.value.err.startswith("missing")

    add_to["hostname"] = missing
    trivval.validate_dict(value, schema, trivval.FLAG_ALLOW_EXTRA)
    test_extra()


def test_exact() -> None:
    """Test against the same version."""
    for version in sorted(tdata.VALUES.keys()):
        schema = tdata.SCHEMA[version]
        for value in tdata.VALUES[version]:
            do_test(value, schema)


def test_backwards() -> None:
    """Test against an earlier version."""
    for current_version in sorted(tdata.VALUES.keys()):
        for earlier_version in sorted(
            ver
            for ver in tdata.SCHEMA
            if ver[0] == current_version[0] and ver[1] < current_version[1]
        ):
            schema = tdata.SCHEMA[earlier_version]
            for value in tdata.VALUES[current_version]:
                do_test(value, schema, backwards=True)


def test_breaking() -> None:
    """Make sure validation fails after a breaking change."""
    for current_version in sorted(tdata.VALUES.keys()):
        for other_version in sorted(ver for ver in tdata.SCHEMA if ver[0] != current_version[0]):
            schema = tdata.SCHEMA[other_version]
            for value in tdata.VALUES[current_version]:
                with pytest.raises(trivval.ValidationError):
                    trivval.validate_dict(value, schema, 0)


def test_schema() -> None:
    """Make sure validation succeeds with all schemas."""
    called: list[tuple[dict[str, Any], trivval.SchemaType, int] | None] = [None]

    def mock_validate_dict(value: dict[str, Any], schema: trivval.SchemaType, flags: int) -> None:
        called.append((value, schema, flags))

    for version, values in tdata.VALUES.items():
        v_format = {"version": {"major": version[0], "minor": version[1]}}
        for value in values:
            augmented = dict(value)
            assert "format" not in augmented
            augmented["format"] = v_format

            trivval.validate(augmented, tdata.SCHEMA, 0)

            assert augmented["format"] is v_format
            del augmented["format"]
            assert augmented == value

            augmented["format"] = v_format
            called = [None]

            with mock.patch("trivval.validate_dict", new=mock_validate_dict):
                trivval.validate(augmented, tdata.SCHEMA, 0)

            assert called[1] is not None
            assert called[1][0] == augmented
            called.pop(1)
            assert called == [
                None,
                (value, tdata.SCHEMA[version], 0),
            ]  # type: ignore[comparison-overlap]


def test_exact_json() -> None:
    """Test against the same version after a round trip through JSON."""
    for version in sorted(tdata.VALUES.keys()):
        schema = tdata.SCHEMA[version]
        for value in tdata.VALUES[version]:
            do_test(json.loads(json.dumps(value)), schema)


def test_optional() -> None:
    """Test "?key" not present or present as a null value."""
    schema = {"first": str, "?second": int}

    trivval.validate_dict({"first": "hello"}, schema, 0)
    trivval.validate_dict({"first": "hello", "second": None}, schema, 0)
    trivval.validate_dict({"first": "goodbye", "second": 42}, schema, 0)

    with pytest.raises(trivval.ValidationError):
        trivval.validate_dict({"second": 42}, schema, 0)

    with pytest.raises(trivval.ValidationError):
        trivval.validate_dict({"first": "1", "second": "2"}, schema, 0)
