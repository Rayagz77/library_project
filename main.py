from flask import Flask, render_template
from controllers.auth_controller import auth_bp

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Secret key for session security

# Register the blueprint for authentication
app.register_blueprint(auth_bp, url_prefix='/auth')

# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')  # Make sure home.html exists in the 'templates' folder

@app.route('/login')
def login():
    return render_template('login.html')  

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/faq')
def faq():
    return render_template('faq.html') 

if __name__ == '__main__':
    app.run(debug=True)












