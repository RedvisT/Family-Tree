# Remove this line:
import os
from flask import Flask, render_template, request, redirect, url_for, flash

import sqlite3
from database_files import DATABASE
import database_files  # Import your database file

app = Flask(__name__)
# Set the secret key to enable session and flash functionality
app.secret_key = os.urandom(24)  # Or use a fixed string for production

# Route for displaying the signup page (GET method)
@app.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')

# Route for handling the form submission (POST method)
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Check if passwords match
    if password != confirm_password:
        return render_template('signup.html', error_message="Passwords do not match!")


    # Insert user into the database (you may want to hash the password before saving it)
    try:
        # Try to insert the user into the database
        user_created = database_files.insert_user(username, password)
        if user_created:
            return render_template('signup.html', success_message="Account created successfully! You can now log in.")

        else:
            return render_template('signup.html', error_message="Username already exists!")

    except sqlite3.Error:
        return render_template('signup.html', error_message="Database connection error, please try again later.")


# Route for displaying the login page (GET method)
@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

# Route for handling login (POST method)
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if username and password match in the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()

    if user:
        return redirect(url_for('home', success_message="Logged in successfully!"))

    else:
        return render_template('login.html', error_message="Invalid credentials. Please try again.")


if __name__ == '__main__':
    app.run(debug=True)
