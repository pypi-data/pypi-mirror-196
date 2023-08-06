# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Data samples for the validation library tests."""

from __future__ import annotations


SCHEMA_1_0 = {
    "node": {
        "hostname": str,
        "flavor": {"desktop", "laptop", "server"},
        "services": {
            "launcher": {"timestamp": int},
            "server": {"timestamp": int, "instances": int},
        },
    },
    "users": {"*": {"first_name": str, "last_name": str, "id": int}},
    "tags": [str],
}

SCHEMA_1_1 = {
    "node": {
        "hostname": str,
        "flavor": {"desktop", "laptop", "server"},
        "services": {
            "launcher": {"timestamp": int},
            "server": {"timestamp": int, "instances": int},
        },
    },
    "users": {"*": {"first_name": str, "last_name": str, "id": int, "?nickname": str}},
    "tags": [str],
}

SCHEMA_2_0 = {
    "nodes": {
        "*": {
            "hostname": str,
            "flavor": {"laptop", "server"},
            "services": {
                "launcher": {"timestamp": int},
                "server": {"timestamp": int, "instances": int},
            },
        },
    },
    "users": {
        "*": {
            "first_name": str,
            "last_name": str,
            "id": int,
            "?nickname": str,
        }
    },
    "tags": [str],
}

SCHEMA = {
    (1, 0): SCHEMA_1_0,
    (1, 1): SCHEMA_1_1,
    (2, 0): SCHEMA_2_0,
}

VALUES_1_0 = [
    {
        "node": {
            "hostname": "straylight",
            "flavor": "laptop",
            "services": {
                "launcher": {"timestamp": 1000},
                "server": {"timestamp": 1001, "instances": 4},
            },
        },
        "users": {
            "jrl": {
                "first_name": "J. Random",
                "last_name": "Lucretius",
                "id": 42,
            },
            "centre": {"first_name": "Aza", "last_name": "Thoth", "id": 616},
        },
        "tags": ["foo", "bar"],
    },
    {
        "node": {
            "hostname": "feylight",
            "flavor": "desktop",
            "services": {
                "launcher": {"timestamp": 3000},
                "server": {"timestamp": 3005, "instances": 4},
            },
        },
        "users": {
            "guest": {
                "first_name": "Mister",
                "last_name": "Apollinax",
                "id": 201,
            },
        },
        "tags": [],
    },
]

VALUES_1_1 = [
    {
        "node": {
            "hostname": "straylight",
            "flavor": "server",
            "services": {
                "launcher": {"timestamp": 1000},
                "server": {"timestamp": 1001, "instances": 4},
            },
        },
        "users": {
            "jrl": {
                "first_name": "J. Random",
                "last_name": "Lucretius",
                "id": 42,
                "nickname": "jay",
            },
            "centre": {"first_name": "Aza", "last_name": "Thoth", "id": 616},
        },
        "tags": ["foo", "bar"],
    },
    {
        "node": {
            "hostname": "feylight",
            "flavor": "desktop",
            "services": {
                "launcher": {"timestamp": 3000},
                "server": {"timestamp": 3005, "instances": 4},
            },
        },
        "users": {
            "guest": {
                "first_name": "Mister",
                "last_name": "Apollinax",
                "id": 201,
                "nickname": "paul",
            },
        },
        "tags": [],
    },
]

VALUES_2_0 = [
    {
        "nodes": {
            "laptop": {
                "hostname": "straylight",
                "flavor": "laptop",
                "services": {
                    "launcher": {"timestamp": 1000},
                    "server": {"timestamp": 1001, "instances": 4},
                },
            },
        },
        "users": {
            "jrl": {
                "first_name": "J. Random",
                "last_name": "Lucretius",
                "id": 42,
                "nickname": "jay",
            },
            "centre": {"first_name": "Aza", "last_name": "Thoth", "id": 616},
        },
        "tags": ["foo", "bar"],
    },
    {
        "nodes": {
            "local": {
                "hostname": "feylight",
                "flavor": "server",
                "services": {
                    "launcher": {"timestamp": 3000},
                    "server": {"timestamp": 3005, "instances": 4},
                },
            },
        },
        "users": {
            "guest": {
                "first_name": "Mister",
                "last_name": "Apollinax",
                "id": 201,
                "nickname": "paul",
            },
        },
        "tags": [],
    },
]

VALUES = {
    (1, 0): VALUES_1_0,
    (1, 1): VALUES_1_1,
    (2, 0): VALUES_2_0,
}
