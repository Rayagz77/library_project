SECRET_KEY = 'supersecretkey'  #secure the session of the login
# config.py

import os

class Config:
    # Hugging Face API key
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "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")

    # Secret key for Flask sessions
    SECRET_KEY = 'your_secret_key'

    # Email settings for Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'  # For example, using Gmail SMTP server
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "your_email@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "your_email_password")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "your_email@gmail.com")

