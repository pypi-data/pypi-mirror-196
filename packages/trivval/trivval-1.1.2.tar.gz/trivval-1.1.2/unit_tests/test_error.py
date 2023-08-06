# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Trivial tests for the ValidationError class."""

from __future__ import annotations

import trivval


def test_error_string() -> None:
    """Test the stringification of the error."""
    messages = (
        ["word"],
        ["two words"],
        ["two", "words"],
        ["slash/phrase", "and: more"],
    )

    for msg in messages:
        joined = "\t".join(msg)
        err = trivval.ValidationError([], joined)
        assert str(err) == joined

    for key in messages:
        for msg in messages:
            slashed = "/".join(key)
            joined = "\t".join(msg)
            err = trivval.ValidationError(key, joined)
            assert str(err) == f"{joined}: {slashed}"
