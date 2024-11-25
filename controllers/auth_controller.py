from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

# Create a blueprint for handling authentication routes
auth_bp = Blueprint('auth', __name__)

# List of users (in-memory)
users = []

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find user in the list
        user = next((user for user in users if user['username'] == username), None)

        if user and check_password_hash(user['password'], password):
            session['username'] = username  # Store the username in the session
            return redirect(url_for('home'))  # Redirect to the homepage
        else:
            flash('Invalid credentials', 'error')

    return render_template('login.html')

from flask import Blueprint, render_template, request, redirect, url_for, flash

auth_controller = Blueprint('auth_controller', __name__)

users = []  # Temporary storage for users

@auth_controller.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        consent = request.form.get('consent')

        if not all([first_name, last_name, email, username, password, consent]):
            flash("All fields are required.", "error")
            return redirect(url_for('auth_controller.signup'))

        users.append({'first_name': first_name, 'last_name': last_name, 'email': email, 'username': username})
        flash("Signup successful!", "success")
        return redirect(url_for('auth_controller.login'))

    return render_template('signup.html')


       