import sqlite3
from flask import g

DATABASE = r"C:\Users\Redvis\Documents\A Database\FamilyHistory.db"

def get_db():
    """Connect to the SQLite database."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Allows access to columns by name
    return g.db

def close_db(e=None):
    """Close the database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def insert_user(username, password):
    """Insert a new user into the database."""
    db = get_db()
    try:
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        return True, None  # Return a tuple indicating success and no error message
    except sqlite3.IntegrityError:  # Handle the case where the username already exists
        return False, "Username already exists"
    finally:
        close_db()

def check_user_credentials(username, password):
    """Check if the username and password are correct."""
    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    close_db()  # Ensure the database connection is closed after the operation
    return user  # Return the user record if found, or None if not found
