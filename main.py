from flask import Flask, render_template
from flask_mail import Mail
from config import Config
from controllers.auth_controller import auth_bp
from controllers.text_generation_controller import text_generation_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)  # Load configuration, including SECRET_KEY and Mail settings

# Initialize Flask-Mail
mail = Mail(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(text_generation_bp, url_prefix='/text-generation')

# Routes for main pages
@app.route('/')
def home():
    return render_template('home.html')  # Ensure home.html exists in the 'templates' folder

@app.route('/login')
def login():
    return render_template('login.html')  # Ensure login.html exists in the 'templates' folder

@app.route('/signup')
def signup():
    return render_template('signup.html')  # Ensure signup.html exists in the 'templates' folder

@app.route('/faq')
def faq():
    return render_template('faq.html')  # Ensure faq.html exists in the 'templates' folder

# Run the application
if __name__ == '__main__':
    app.run(debug=True)



