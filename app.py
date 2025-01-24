from flask import Flask, render_template, request, redirect, url_for, flash, session
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
            session['username'] = username  # Store username in session
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

# Route to add family member
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        birthdate = request.form['Birthdate']
        deathdate = request.form['Deathdate']
        gender = request.form['Gender']
        place_of_birth = request.form['PlaceOfBirth']
        photo = request.files['Photo'].read() if 'Photo' in request.files else None

        # Extract family relationships
        biological_father_id = request.form['BiologicalFatherID']
        stepfather_id = request.form['StepfatherID']
        mother_id = request.form['MotherID']
        stepmother_id = request.form['StepMotherID']
        current_spouse_id = request.form['CurrentSpouseID']
        divorced_spouse_id = request.form['DivorcedSpouseID']
        adoptive_father_id = request.form['AdoptiveFatherID']
        adoptive_mother_id = request.form['AdoptiveMotherID']
        biological_mother_id = request.form['BiologicalMotherID']

        # Add member to the database
        db = database_files.get_db()
        db.execute('''
            INSERT INTO FamilyTree (FirstName, LastName, Birthdate, Deathdate, Gender, PlaceOfBirth, Photo,
                                    BiologicalFatherID, StepfatherID, MotherID, StepMotherID, CurrentSpouseID,
                                    DivorcedSpouseID, AdoptiveFatherID, AdoptiveMotherID, BiologicalMotherID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, birthdate, deathdate, gender, place_of_birth, photo,
              biological_father_id, stepfather_id, mother_id, stepmother_id, current_spouse_id,
              divorced_spouse_id, adoptive_father_id, adoptive_mother_id, biological_mother_id))
        db.commit()
        database_files.close_db()

        # Redirect back to the family tree page
        return redirect(url_for('family_tree'))

    return render_template('add_member.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
