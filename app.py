from flask import Flask, redirect, render_template, session, url_for
import os
from page_handler import page_handler  # Import the blueprint
import database_files

# Initialize the Flask app
app = Flask(__name__)

# Set the secret key to enable session and flash functionality
app.secret_key = os.urandom(24)  # Or use a fixed string for production

# Register the blueprint
app.register_blueprint(page_handler)

# Route to initialize the database
@app.route('/init_db')
def initialize_database():
    database_files.init_db()
    return "Database initialized!"

# Home route that renders the login page
@app.route('/')
def home():
    return render_template('login.html')

# Family home route (after login success)
@app.route('/family_home')
def family_home():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('index.html')

# Introduction page route
@app.route('/introduction')
def introduction():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('introduction.html')

# Family tree page route
@app.route('/family_tree')
def family_tree():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('family_tree.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
