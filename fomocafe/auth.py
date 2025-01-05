from datetime import datetime

import jwt
import sqlite3
from flask import current_app
from flask_login import LoginManager

from fomocafe.models import User

login_manager = LoginManager()

@login_manager.request_loader
def load_user_from_request(request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return None

    token = auth_header.replace("Bearer ", "")
    if token is None or len(token) == 0:
        return None

    try:
        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        result = cur.execute(
            "SELECT id, name, email, username, created, updated "
            "FROM users "
            "WHERE username = ?",
            (payload["sub"],),
        ).fetchone()
        if result is None:
            return None
    return User(
        id=result[0],
        name=result[1],
        email=result[2],
        username=result[3],
        password=None,
        created=datetime.fromisoformat(result[4]),
        updated=datetime.fromisoformat(result[4]),
    )
