import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, session
import database_files  # Import the database functions
import os
import validation

# Initialize the Flask app
app = Flask(__name__)

# Set the secret key to enable session and flash functionality
app.secret_key = os.urandom(24)  # Or use a fixed string for production

# Home route that renders the login page
@app.route('/')
def home():
    return render_template('login.html')

# Login route for user login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists and retrieve the hashed password
        user = database_files.get_user_by_username(username)
        if user:
            stored_hashed_password = user['password']
            # Verify the entered password against the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                session['username'] = username  # Store username in session
                return redirect(url_for('family_home'))
            else:
                return render_template('login.html', alert_message="Invalid username or password", alert_type="error")
        else:
            return render_template('login.html', alert_message="Invalid username or password", alert_type="error")

    return render_template('login.html')

# Signup route for creating a new user account
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        birthdate = request.form['birthdate']
        gender = request.form['gender']

        # Validate the user data
        validation_errors, middle_name = validation.validate_user_data(username, password, confirm_password, first_name, middle_name, last_name, birthdate, gender)
        if validation_errors:
            return render_template('signup.html', error_messages=validation_errors, username=username,
                                   first_name=first_name, middle_name=middle_name, last_name=last_name,
                                   birthdate=birthdate, gender=gender)

        # Check if passwords match
        if password != confirm_password:
            return render_template('signup.html', error_message="Passwords do not match", username=username,
                                   first_name=first_name, middle_name=middle_name, last_name=last_name,
                                   birthdate=birthdate, gender=gender)

        # Hash and salt the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert the user into the database with the hashed password
        success, message = database_files.insert_user(username, hashed_password.decode('utf-8'), first_name, middle_name, last_name, birthdate, gender)
        if success:
            return redirect(url_for('home', message="Account created successfully! You can now log in."))
        else:
            return render_template('signup.html', error_message=message, username=username,
                                   first_name=first_name, middle_name=middle_name, last_name=last_name,
                                   birthdate=birthdate, gender=gender)

    return render_template('signup.html')

# Family home route (after login success)
@app.route('/family_home')
def family_home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Introduction page route
@app.route('/introduction')
def introduction():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('introduction.html')

# Family tree page route
@app.route('/family_tree')
def family_tree():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('family_tree.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
