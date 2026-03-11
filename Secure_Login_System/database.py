"""
database.py - Handles SQLite database setup and user operations

DATABASE SCHEMA:
    users table:
        id       - INTEGER PRIMARY KEY (auto-incremented unique identifier)
        username - TEXT, unique and required
        password - TEXT, stores the HASHED password (never plain text!)

WHY NOT STORE PLAIN TEXT PASSWORDS?
    If an attacker breaches your database and passwords are plain text,
    they instantly have access to ALL user accounts — including on other
    sites where users reuse passwords. Hashing is a one-way transformation,
    so even database admins cannot read the original password.
"""

import sqlite3

# Path to our SQLite database file
DB_PATH = "users.db"


def get_connection():
    """Open and return a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """
    Create the users table if it doesn't already exist.
    Called once at app startup.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL
        )
    """)
    # 'password' here stores the bcrypt hash+salt string, e.g.:
    #   $2b$12$KIXoRzBl3J1u7oVDCexQfuK6n8Qw...  (60 chars)

    conn.commit()
    conn.close()
    print("[DB] Database initialized — users table ready.")


def add_user(username, hashed_password):
    """
    Insert a new user into the database.

    Args:
        username        (str): The chosen username.
        hashed_password (bytes): The bcrypt hash of the password.

    Returns:
        True if successful, False if username already exists.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Store the hash as a string (decode from bytes → str)
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password.decode("utf-8"))
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # UNIQUE constraint failed — username already taken
        return False


def get_user(username):
    """
    Fetch a user record by username.

    Args:
        username (str): The username to look up.

    Returns:
        A dict with 'id', 'username', 'password' — or None if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"id": row[0], "username": row[1], "password": row[2]}
    return None
