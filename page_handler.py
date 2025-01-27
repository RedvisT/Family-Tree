from flask import Blueprint, render_template, request, redirect, session, url_for, flash
import database_files
import bcrypt

import validation

# Initialize the blueprint
page_handler = Blueprint('page_handler', __name__)

# Route to render the children.html page
@page_handler.route('/add_children', methods=['GET'])
def add_children_form():
    return render_template('children.html')

# Route for displaying the signup page (GET method)
@page_handler.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')

# Route for handling the form submission (POST method)
@page_handler.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    birthdate = request.form['birthdate']
    gender = request.form['gender']

    # Check if passwords match
    if password != confirm_password:
        return render_template('signup.html', error_message="Passwords do not match!", username=username,
                               first_name=first_name, middle_name=middle_name, last_name=last_name,
                               birthdate=birthdate, gender=gender)

    # Set middle name to "N/A" if empty
    if not middle_name:
        middle_name = "N/A"

    # Validate the user data
    validation_errors, middle_name = validation.validate_user_data(username, password, confirm_password, first_name, middle_name, last_name, birthdate, gender)
    if validation_errors:
        return render_template('signup.html', error_messages=validation_errors, username=username,
                               first_name=first_name, middle_name=middle_name, last_name=last_name,
                               birthdate=birthdate, gender=gender)

    # Hash and salt the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert user into the database (with hashed password)
    success, message = database_files.insert_user(username, hashed_password.decode('utf-8'),
                                                   first_name, middle_name, last_name, birthdate, gender)
    if success:
        return redirect(url_for('home', message="Account created successfully! You can now log in."))
    else:
        return render_template('signup.html', error_message=message, username=username,
                               first_name=first_name, middle_name=middle_name, last_name=last_name,
                               birthdate=birthdate, gender=gender)

# Route for handling login (POST method)
@page_handler.route('/login', methods=['POST', 'GET'])
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
                return render_template('login.html', error_message="Invalid username or password. Please try again.")
        else:
            return render_template('login.html', error_message="Invalid username or password. Please try again.")

    return render_template('login.html')
