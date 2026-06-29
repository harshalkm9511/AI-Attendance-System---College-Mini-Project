from __future__ import annotations

from functools import wraps

from flask import g

from .db import query_one


def load_logged_in_user() -> None:
    default_tenant_code = g.get("default_tenant_code", "demo-institute")
    g.user = query_one(
        """
        SELECT users.*, tenants.name AS tenant_name, tenants.code AS tenant_code
        FROM users
        JOIN tenants ON tenants.id = users.tenant_id
        WHERE tenants.code = ?
        ORDER BY users.id ASC
        LIMIT 1
        """,
        (default_tenant_code,),
    )


def login_user(username: str, password: str) -> bool:
    return True


def logout_user() -> None:
    return None


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        return view(**kwargs)

    return wrapped_view
