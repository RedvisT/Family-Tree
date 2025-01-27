import re

def is_valid_name(name):
    return re.match(r'^[A-Za-z ]+$', name) is not None

def is_valid_birthdate(birthdate):
    return re.match(r'^\d{2}/\d{2}/\d{4}$', birthdate) is not None

def validate_user_data(username, password, confirm_password, first_name, middle_name, last_name, birthdate, gender):
    errors = []

    if not is_valid_name(first_name):
        errors.append("Invalid first name. Only letters and spaces are allowed.")

    if middle_name == "":
        middle_name = "N/A"
    elif middle_name != "N/A" and not is_valid_name(middle_name):
        errors.append("Invalid middle name. Only letters and spaces are allowed.")

    if not is_valid_name(last_name):
        errors.append("Invalid last name. Only letters and spaces are allowed.")

    if not is_valid_birthdate(birthdate):
        errors.append("Invalid birthdate format. Use DD/MM/YYYY.")

    # Additional checks for other fields can be added here

    return errors, middle_name


    # Additional checks for other fields can be added here

    return errors, middle_name
