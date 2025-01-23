from flask import Flask, flash, render_template, request, redirect, url_for
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
@app.route('/login', methods=['POST', 'GET'])  # Allow both GET and POST methods
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid
        user = database_files.check_user_credentials(username, password)
        if user:
            return redirect(url_for('family_home'))  # Redirect to family home page after successful login
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

# Signup route for creating a new user account
@app.route('/signup', methods=['POST', 'GET'])  # Handle GET and POST requests for signup
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match")  # Flash the error message
            return render_template('signup.html')

        # Insert the user into the database
        success = database_files.insert_user(username, password)
        if success:
            flash("Account created successfully! You can now log in.")  # Flash success message
            return redirect(url_for('login'))  # Redirect to login page after successful signup
        else:
            flash("Username already exists")  # Flash error message
            return render_template('signup.html')

    return render_template('signup.html')


# Family home route (after login success)
@app.route('/family_home')
def family_home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
