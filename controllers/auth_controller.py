from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models_new.user_model import User
from models_new import db
from datetime import datetime
import re

# Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# --- Login Route ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find user in the database by username
        user = User.query.filter_by(user_email=username).first()

        if user and check_password_hash(user.user_password, password):
            session['username'] = username  # Store the username in the session
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to the homepage
        else:
            flash('Invalid credentials', 'error')

    return render_template('login.html')

# --- Signup Route ---
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        username = request.form.get('username')  # Used as email in this case
        password = request.form.get('password')
        phone_number = request.form.get('phone_number')
        consent = request.form.get('consent')

        # Server-side validation
        if not all([first_name, last_name, email, username, password, consent]):
            flash("All fields are required, including consent.", "error")
            return redirect(url_for('auth.signup'))

        if len(first_name) < 3 or len(last_name) < 3:
            flash("First name and last name must be at least 3 characters.", "error")
            return redirect(url_for('auth.signup'))

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            flash("Please enter a valid email address.", "error")
            return redirect(url_for('auth.signup'))

        if len(password) < 12:
            flash("Password must be at least 12 characters.", "error")
            return redirect(url_for('auth.signup'))

        phone_pattern = r"^\+?\d{7,15}$"
        if phone_number and not re.match(phone_pattern, phone_number):
            flash("Please enter a valid phone number.", "error")
            return redirect(url_for('auth.signup'))

        # Check if the email already exists
        existing_user = User.query.filter_by(user_email=email).first()
        if existing_user:
            flash("This email is already in use.", "error")
            return redirect(url_for('auth.signup'))

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Create a new user in the database
        new_user = User(
            user_firstname=first_name,
            user_lastname=last_name,
            user_email=email,
            user_signup_date=datetime.utcnow(),
            user_password=hashed_password,
            user_phone=phone_number
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Signup successful! You can now log in.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error during signup: {str(e)}", "error")
            return redirect(url_for('auth.signup'))

    return render_template('signup.html')

# --- Logout Route ---
@auth_bp.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')  # Remove username from session
        flash("You have been logged out.", "success")
    else:
        flash("You are not logged in.", "info")
    return redirect(url_for('auth.login'))



       