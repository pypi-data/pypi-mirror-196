# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Trivial validation - when the full power of the JSON Schema is not needed.

This library provides a simplistic way to validate a dictionary against
something resembling a schema - a dictionary describing the desired data
structure by example.

The main entry point is the validate() function, but the various
validate_*() functions may be invoked directly with appropriate
arguments.

The schema used for validation is a dictionary (the top-level object must
be a dictionary). For the present, the keys may only be strings.
A special case of a dictionary with a single key "*" means any value for
a key will be accepted. Otherwise, all keys with names not starting with
a "?" character are mandatory, and any keys with names starting with
a "?" character are optional (or may be present with null values).

The dictionary values may be any of:
- a Python type signifying that the value must be an instance thereof
- a single-element list signifying that the value must be a list with
  all the elements validated by the same rules as a dictionary value
  (i.e. one of a Python type, a single-element list, a set, or
  a dictionary)
- a set signifying that the value must be exactly equal to one of
  the set elements, i.e. an enumeration of the allowed values
- a dictionary with the same semantics as described above

For example, the following schema:

    {
        "name": str,
        "id": int,
        "address": [str],
        "preferences": {
            "meal": set(("breakfast", "lunch", "brunch")),
            "colors": [{
                "name": str,
                "intensity": set(["dark", "light"]),
                "?weight": int,
            }]
        },
        "possessions": {
            "*": int
        }
    }

...may be used to validate the following dictionary:

    {
        "name": "A. N. Nymous",
        "id": 13,
        "address": [
            "42 Nowhere Circle",
            "Notown-at-all",
            "Unnamed territory"
        ],
        "preferences": {
            "meal": "brunch",
            "colors": [
                {"name": "blue", "intensity": "light"},
                {"name": "green", "intensity": "dark", "weight": None},
                {"name": "red", "intensity": "light", "weight": 75},
            ]
        },
        "possessions": {
            "pencil": 4,
            "paper": 0
        }
    }
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

VERSION = "1.1.2"

FEATURES_STRING = "trivval=" + VERSION

FLAG_ALLOW_EXTRA = 0x0001

SCHEMA_FORMAT = {"format": {"version": {"major": int, "minor": int}}}

SchemaType = Dict[Tuple[int, int], Dict[str, Any]]


class ValidationError(Exception):
    """Signal an error that occurred during the validation."""

    def __init__(self, path: list[str], err: str) -> None:
        """Store the path and the error message, build the message to be displayed."""
        self.path = path
        self.err = err
        suffix = "" if not self.path else ": " + "/".join(path)
        super().__init__(err + suffix)


def validate_single(key: str, item: Any, schema: Any, flags: int) -> None:  # noqa: ANN401
    """Validate a single dictionary value."""
    if isinstance(schema, type):
        if not isinstance(item, schema):
            raise ValidationError(
                [key],
                f"not a {schema.__name__}, {type(item).__name__} instead",
            )
    elif isinstance(schema, list):
        validate_list(key, item, schema, flags)
    elif isinstance(schema, set):
        if item not in schema:
            raise ValidationError([key], "not among the allowed values")
    elif isinstance(schema, dict):
        try:
            validate_dict(item, schema, flags)
        except ValidationError as err:
            raise ValidationError([key, *err.path], err.err) from err
    else:
        raise ValidationError([key], f"usage error: invalid schema type {schema!r}")


def validate_list(key: str, value: list[Any], schema: list[Any], flags: int) -> None:
    """Validate a list against a single-element schema."""
    if not isinstance(value, list):
        raise ValidationError([key], f"not a list, {type(value).__name__} instead")

    if len(schema) != 1:
        raise ValidationError([key], f"usage error: schema {schema!r} not a single-element list")
    for index, item in enumerate(value):
        validate_single(
            f"{key}[{index}]",
            item,
            schema[0],
            flags,
        )


def validate_dict(value: Any, schema: dict[str, Any], flags: int) -> None:  # noqa: ANN401
    """Validate a dictionary against a schema."""
    if not isinstance(value, dict):
        raise ValidationError([], f"not a dictionary, {type(value).__name__} instead")

    if len(schema.keys()) == 1 and "*" in schema:
        valtype = schema["*"]
        for key in value:
            validate_single(key, value[key], valtype, flags)
        return

    processed = set()
    for q_key, valtype in schema.items():
        if q_key.startswith("?"):
            key = q_key[1:]
            if value.get(key, None) is None:
                processed.add(key)
                continue
        elif q_key not in value:
            raise ValidationError([q_key], "missing")
        else:
            key = q_key

        processed.add(key)
        validate_single(key, value[key], valtype, flags)

    extra = set(value.keys()) - processed
    if extra and not flags & FLAG_ALLOW_EXTRA:
        raise ValidationError([",".join(sorted(extra))], "extra keys")


def validate(value: dict[str, Any], schemas: SchemaType, flags: int = 0) -> None:
    """Validate a dictionary against the appropriate schema."""
    try:
        validate_dict(value, SCHEMA_FORMAT, FLAG_ALLOW_EXTRA)
    except (AttributeError, KeyError, TypeError, ValueError) as err:
        raise ValidationError(
            ["format", "version"],
            "could not parse the version of the data format",
        ) from err
    version = (
        value["format"]["version"]["major"],
        value["format"]["version"]["minor"],
    )
    stripped = {key: val for key, val in value.items() if key != "format"}

    same_major = sorted(ver for ver in schemas if ver[0] == version[0] and ver[1] <= version[1])
    if not same_major:
        raise ValidationError(["format", "version"], "unsupported format version")

    validate_dict(stripped, schemas[same_major[-1]], flags)
