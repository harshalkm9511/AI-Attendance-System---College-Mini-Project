from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterable

from flask import current_app, g
from werkzeug.security import generate_password_hash


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS tenants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE (tenant_id, username)
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    roll_no TEXT NOT NULL,
    department TEXT DEFAULT '',
    section_name TEXT DEFAULT '',
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (tenant_id, roll_no)
);

CREATE TABLE IF NOT EXISTS student_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    face_path TEXT NOT NULL,
    embedding_json TEXT NOT NULL,
    embedding_provider TEXT NOT NULL,
    quality_score REAL NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS attendance_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    classroom_image_path TEXT NOT NULL,
    annotated_image_path TEXT DEFAULT '',
    status TEXT NOT NULL,
    faces_detected INTEGER NOT NULL DEFAULT 0,
    matched_count INTEGER NOT NULL DEFAULT 0,
    uncertain_count INTEGER NOT NULL DEFAULT 0,
    unknown_count INTEGER NOT NULL DEFAULT 0,
    created_by INTEGER REFERENCES users(id),
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL,
    finalized_at TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS detected_faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL REFERENCES attendance_sessions(id) ON DELETE CASCADE,
    face_index INTEGER NOT NULL,
    bbox_json TEXT NOT NULL,
    face_path TEXT NOT NULL,
    embedding_json TEXT NOT NULL,
    embedding_provider TEXT NOT NULL,
    best_student_id INTEGER REFERENCES students(id),
    match_score REAL NOT NULL DEFAULT 0,
    status TEXT NOT NULL,
    reviewed_student_id INTEGER REFERENCES students(id),
    review_notes TEXT DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS attendance_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL REFERENCES attendance_sessions(id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    status TEXT NOT NULL,
    confidence REAL NOT NULL DEFAULT 0,
    marked_at TEXT NOT NULL,
    UNIQUE (session_id, student_id)
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id INTEGER,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


def utcnow() -> str:
    return datetime.utcnow().isoformat(timespec="seconds")


def row_to_dict(row: sqlite3.Row | None) -> dict | None:
    if row is None:
        return None
    return {key: row[key] for key in row.keys()}


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        db_path = Path(current_app.config["DATABASE_PATH"])
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        g.db = conn
    return g.db


def close_db(_error=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


@contextmanager
def transaction():
    db = get_db()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise


def init_db() -> None:
    db = get_db()
    db.executescript(SCHEMA)
    seed_defaults(db)
    db.commit()


def seed_defaults(db: sqlite3.Connection) -> None:
    config = current_app.config
    now = utcnow()
    tenant = db.execute("SELECT id FROM tenants WHERE code = ?", (config["DEFAULT_TENANT_CODE"],)).fetchone()
    if tenant is None:
        db.execute(
            "INSERT INTO tenants (name, code, created_at) VALUES (?, ?, ?)",
            (config["DEFAULT_TENANT_NAME"], config["DEFAULT_TENANT_CODE"], now),
        )
        tenant = db.execute("SELECT id FROM tenants WHERE code = ?", (config["DEFAULT_TENANT_CODE"],)).fetchone()

    db.execute(
        """
        INSERT OR IGNORE INTO users (tenant_id, username, password_hash, role, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            tenant["id"],
            config["DEFAULT_ADMIN_USERNAME"],
            generate_password_hash(config["DEFAULT_ADMIN_PASSWORD"]),
            "super_admin",
            now,
        ),
    )


def log_action(tenant_id: int, user_id: int | None, action: str, entity_type: str, entity_id: int | None, payload: dict) -> None:
    db = get_db()
    db.execute(
        """
        INSERT INTO audit_logs (tenant_id, user_id, action, entity_type, entity_id, payload_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (tenant_id, user_id, action, entity_type, entity_id, json.dumps(payload), utcnow()),
    )
    db.commit()


def query_all(sql: str, params: Iterable = ()) -> list[dict]:
    rows = get_db().execute(sql, tuple(params)).fetchall()
    return [row_to_dict(row) for row in rows]


def query_one(sql: str, params: Iterable = ()) -> dict | None:
    return row_to_dict(get_db().execute(sql, tuple(params)).fetchone())
