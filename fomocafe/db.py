import sqlite3
from flask import Flask


def init_app(app: Flask):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        username TEXT UNIQUE,
        password TEXT,
        name TEXT,
        role TEXT,
        created TEXT,
        updated TEXT
    )
    """,
    )
    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        category TEXT,
        price REAL,
        stock INTEGER,
        image_url TEXT,
        created TEXT,
        updated TEXT
    )
    """,
    )
    con.commit()
    con.close()
