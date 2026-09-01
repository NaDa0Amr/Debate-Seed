"""Shared PostgreSQL configuration and connection helpers."""

from __future__ import annotations

import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

_ENV_TO_CONNECT_KEY = {
    "PGHOST": "host",
    "PGPORT": "port",
    "PGDATABASE": "dbname",
    "PGUSER": "user",
    "PGPASSWORD": "password",
}


def get_db_config(*, purpose: str = "the pipeline") -> dict[str, str]:
    values = {name: os.environ.get(name) for name in _ENV_TO_CONNECT_KEY}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise RuntimeError(
            "Missing PostgreSQL configuration env vars: "
            + ", ".join(missing)
            + f". Set them before running {purpose}."
        )
    return {
        connect_key: str(values[env_name])
        for env_name, connect_key in _ENV_TO_CONNECT_KEY.items()
    }


def connect(*, purpose: str = "the pipeline", statement_timeout_ms: int | None = None):
    kwargs: dict[str, object] = get_db_config(purpose=purpose)
    kwargs["connect_timeout"] = 10
    if statement_timeout_ms is not None:
        if statement_timeout_ms <= 0:
            raise ValueError("statement_timeout_ms must be > 0")
        kwargs["options"] = f"-c statement_timeout={statement_timeout_ms}"
    return psycopg2.connect(**kwargs)
