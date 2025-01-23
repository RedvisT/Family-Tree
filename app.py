from flask import Flask, render_template, request, redirect, url_for, flash
import database_files  # Import the database functions
import os

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

        # Check if the username and password are valid
        user = database_files.check_user_credentials(username, password)
        if user:
            return redirect(url_for('family_home'))  # Redirect to family home page after successful login
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

        # Check if passwords match
        if password != confirm_password:
            return render_template('signup.html', error_message="Passwords do not match", username=username)

        # Insert the user into the database
        success, message = database_files.insert_user(username, password)
        if success:
            return redirect(url_for('home', message="Account created successfully! You can now log in."))
        else:
            return render_template('signup.html', error_message=message, username=username)

    return render_template('signup.html')

# Family home route (after login success)
@app.route('/family_home')
def family_home():
    return render_template('index.html')

# Introduction page route
@app.route('/introduction')
def introduction():
    return render_template('introduction.html')

# Family tree page route
@app.route('/family_tree')
def family_tree():
    return render_template('family_tree.html')

if __name__ == '__main__':
    app.run(debug=True)