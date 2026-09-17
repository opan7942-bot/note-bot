import sqlite3
import os

"""
Database initialization and CRUD operations module.
Handles sqlite database operations for Notes, Todos, Secrets.
"""


def get_db_path():
    """حفظ قاعدة البيانات في مجلد AppData الخاص بنظام الويندوز لحل مشاكل سطح المكتب والـ EXE"""
    # جلب مسار مجلد AppData الخاص بالمستخدم الحالي
    user_appdata = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))

    # إنشاء مجلد ثابت باسم برنامجك داخل AppData
    app_folder = os.path.join(user_appdata, "MyDesktopApp")
    data_dir = os.path.join(app_folder, "data")

    # التأكد من وجود المجلد
    os.makedirs(data_dir, exist_ok=True)

    return os.path.join(data_dir, "my_bot_data.db")

def init_db():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    # 1. Notes Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER NOT NULL,
            text TEXT NOT NULL
        )
    """)

    # 2. Todos Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER NOT NULL,
            task TEXT,
            status INTEGER NOT NULL DEFAULT 0 
        )
    """)

    # 3. Secrets Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secrets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER NOT NULL,
            title TEXT,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

# --- NOTES ---

def add_note_data(owner_id,text):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (text,owner_id) VALUES (?,?)", (text,owner_id))
    conn.commit()
    conn.close()

def get_notes_data(owner_id):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT id, owner_id, text FROM notes WHERE owner_id = ?",(owner_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_note_data(owner_id,note_id):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE (id,owner_id) = (?,?)", (note_id,owner_id))
    conn.commit()
    conn.close()

# --- TODOS ---

def add_todo_data(owner_id,task):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task,owner_id) VALUES (?,?)", (task,owner_id))
    conn.commit()
    conn.close()

def get_todos_data(owner_id):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT id,owner_id, task FROM todos WHERE owner_id = ?",(owner_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_todo_data(owner_id,todo_id):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE (id,owner_id) = (?,?)", (todo_id,owner_id))
    conn.commit()
    conn.close()

# --- SECRETS ---

def add_secret_data(title, password, owner_id):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("INSERT INTO secrets (title, password,owner_id) VALUES (?, ?,?)", (title, password,owner_id))
    conn.commit()
    conn.close()

def get_secret_data(owner_id):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT id, owner_id,title, password FROM secrets WHERE owner_id = ?",(owner_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_secret_data(owner_id,secret_id):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("DELETE FROM secrets WHERE (id,owner_id) = (?,?)", (secret_id,owner_id))
    conn.commit()
    conn.close()

