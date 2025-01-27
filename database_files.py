import sqlite3
from flask import g, current_app
import bcrypt
from flask import Blueprint, render_template

# Initialize the blueprint
page_handler = Blueprint('page_handler', __name__)

# Route to render the children.html page
@page_handler.route('/add_children', methods=['GET'])
def add_children_form():
    return render_template('children.html')

# Add other routes specific to this blueprint if necessary


DATABASE = r"C:\Users\Redvis\Documents\A Database\FamilyHistory.db"

def get_db():
    """Connect to the SQLite database."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, timeout=10)  # Set a timeout of 10 seconds
        g.db.row_factory = sqlite3.Row  # Allows access to columns by name
    return g.db

def close_db(e=None):
    """Close the database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database and create tables if they do not exist."""
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    close_db()

def get_user_by_username(username):
    """Retrieve a user by username."""
    db = get_db()
    cursor = db.execute('SELECT username, password FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    close_db()  # Ensure the database connection is closed after the operation
    if user:
        return {'username': user['username'], 'password': user['password']}
    else:
        return None

def insert_user(username, hashed_password, first_name, middle_name, last_name, birthdate, gender):
    """Insert a new user into the database."""
    db = get_db()
    try:
        db.execute('INSERT INTO users (username, password, first_name, middle_name, last_name, birthdate, gender) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (username,
                    hashed_password,  # Store the hashed password
                    first_name,
                    middle_name,
                    last_name,
                    birthdate,
                    gender
                   )
                  )
        db.commit()
        return True, None  # Return a tuple indicating success and no error message
    except sqlite3.IntegrityError:  # Handle the case where the username already exists
        return False, "Username already exists"
    finally:
        close_db()

def check_user_credentials(username, password):
    """Check if the username and password are correct."""
    user = get_user_by_username(username)
    if user:
        stored_hashed_password = user['password']
        # Verify the entered password against the stored hashed password
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            return user  # Return the user record if the password is correct
    return None  # Return None if the credentials are invalid
