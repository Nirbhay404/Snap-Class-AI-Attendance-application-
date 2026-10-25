import sqlite3
import os
import bcrypt

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "snapclass.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Auto-initialize database on import
init_db()

def register_teacher(username: str, name: str, password: str, confirm_password: str):
    username = (username or "").strip().lower()
    name = (name or "").strip()
    password = password or ""
    confirm_password = confirm_password or ""

    if not username:
        return False, "Please enter a username."
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if not username.replace("_", "").isalnum():
        return False, "Username can only contain letters, numbers, and underscores."
    if not name:
        return False, "Please enter your full name."
    if not password:
        return False, "Please enter a password."
    if len(password) < 4:
        return False, "Password must be at least 4 characters long."
    if password != confirm_password:
        return False, "Passwords do not match. Please verify both password fields."

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM teachers WHERE username = ?", (username,))
        existing = cursor.fetchone()
        if existing:
            return False, f"Username '{username}' is already taken. Please choose another or login."

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cursor.execute(
            "INSERT INTO teachers (username, name, password_hash) VALUES (?, ?, ?)",
            (username, name, password_hash)
        )
        conn.commit()
        return True, "Teacher profile registered successfully! You can now log in."
    except Exception as e:
        return False, f"Registration error: {str(e)}"
    finally:
        conn.close()

def login_teacher(username: str, password: str):
    username = (username or "").strip().lower()
    password = password or ""

    if not username or not password:
        return False, "Please provide both username and password.", None

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT username, name, password_hash FROM teachers WHERE username = ?", (username,))
        teacher = cursor.fetchone()
        if not teacher:
            return False, "Invalid username or password.", None

        if bcrypt.checkpw(password.encode("utf-8"), teacher["password_hash"].encode("utf-8")):
            return True, f"Welcome back, {teacher['name']}!", {
                "username": teacher["username"],
                "name": teacher["name"]
            }
        else:
            return False, "Invalid username or password.", None
    except Exception as e:
        return False, f"Login error: {str(e)}", None
    finally:
        conn.close()
