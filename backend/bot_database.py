"""SQLite storage for notes, todos, and secrets."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path


_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_db_path() -> str:
    """Return the project's data database path, independent of the launch folder."""
    data_dir = _PROJECT_ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return str(data_dir / "note_bot.db")


@contextmanager
def _connection():
    """Open a connection and always commit/rollback and close it safely."""
    conn = sqlite3.connect(get_db_path())
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Create the application's tables if they do not already exist."""
    with _connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER NOT NULL,
                text TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER NOT NULL,
                task TEXT,
                status INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS secrets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER NOT NULL,
                title TEXT,
                password TEXT
            )
        """)


# Notes
def add_note_data(owner_id, text):
    with _connection() as conn:
        conn.execute("INSERT INTO notes (text, owner_id) VALUES (?, ?)", (text, owner_id))


def get_notes_data(owner_id):
    with _connection() as conn:
        return conn.execute(
            "SELECT id, owner_id, text FROM notes WHERE owner_id = ?", (owner_id,)
        ).fetchall()


def delete_note_data(owner_id, note_id):
    with _connection() as conn:
        cursor = conn.execute("DELETE FROM notes WHERE id = ? AND owner_id = ?", (note_id, owner_id))
        return cursor.rowcount > 0


def update_note_data(owner_id, note_id, text):
    with _connection() as conn:
        cursor = conn.execute(
            "UPDATE notes SET text = ? WHERE id = ? AND owner_id = ?",
            (text, note_id, owner_id),
        )
        return cursor.rowcount > 0


# Todos
def add_todo_data(owner_id, task):
    with _connection() as conn:
        conn.execute("INSERT INTO todos (task, owner_id) VALUES (?, ?)", (task, owner_id))


def get_todos_data(owner_id):
    with _connection() as conn:
        return conn.execute(
            "SELECT id, owner_id, task, status FROM todos WHERE owner_id = ?", (owner_id,)
        ).fetchall()


def complete_todo_data(owner_id, todo_id):
    with _connection() as conn:
        cursor = conn.execute(
            "UPDATE todos SET status = 1 WHERE id = ? AND owner_id = ?",
            (todo_id, owner_id),
        )
        return cursor.rowcount > 0


def update_todo_data(owner_id, todo_id, task):
    with _connection() as conn:
        cursor = conn.execute(
            "UPDATE todos SET task = ? WHERE id = ? AND owner_id = ?",
            (task, todo_id, owner_id),
        )
        return cursor.rowcount > 0


def set_todo_status_data(owner_id, todo_id, status):
    with _connection() as conn:
        cursor = conn.execute(
            "UPDATE todos SET status = ? WHERE id = ? AND owner_id = ?",
            (int(bool(status)), todo_id, owner_id),
        )
        return cursor.rowcount > 0


def delete_todo_data(owner_id, todo_id):
    with _connection() as conn:
        cursor = conn.execute("DELETE FROM todos WHERE id = ? AND owner_id = ?", (todo_id, owner_id))
        return cursor.rowcount > 0


# Secrets
def add_secret_data(title, password, owner_id):
    with _connection() as conn:
        conn.execute(
            "INSERT INTO secrets (title, password, owner_id) VALUES (?, ?, ?)",
            (title, password, owner_id),
        )


def get_secret_data(owner_id):
    with _connection() as conn:
        return conn.execute(
            "SELECT id, owner_id, title, password FROM secrets WHERE owner_id = ?",
            (owner_id,),
        ).fetchall()


def delete_secret_data(owner_id, secret_id):
    with _connection() as conn:
        cursor = conn.execute(
            "DELETE FROM secrets WHERE id = ? AND owner_id = ?", (secret_id, owner_id)
        )
        return cursor.rowcount > 0


def update_secret_data(owner_id, secret_id, title, password):
    with _connection() as conn:
        cursor = conn.execute(
            "UPDATE secrets SET title = ?, password = ? WHERE id = ? AND owner_id = ?",
            (title, password, secret_id, owner_id),
        )
        return cursor.rowcount > 0
