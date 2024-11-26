from flask import Blueprint, request, render_template, current_app
from fpdf import FPDF
import requests
from flask_mail import Message
from io import BytesIO
import logging

# Blueprint for text generation
text_generation_bp = Blueprint('text_generation', __name__)

# Function to generate text using Hugging Face API
def generate_long_text(prompt, min_tokens=2500, max_tokens=3000):
    url = "https://api-inference.huggingface.co/models/gpt-2"
    headers = {
        "Authorization": f"Bearer {current_app.config['HUGGINGFACE_API_KEY']}"
    }
    try:
        response = requests.post(url, headers=headers, json={
            "inputs": prompt,
            "max_length": max_tokens,
            "temperature": 0.7
        }, timeout=30)  # Added timeout
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        result = response.json()
        if isinstance(result, dict) and 'error' in result:
            raise ValueError(f"API Error: {result['error']}")
        return result.get("generated_text", "Error: Text generation failed.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        raise ValueError("Failed to connect to Hugging Face API.") from e

# Function to generate PDF from text
def generate_pdf(text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# Function to send an email with PDF attachment
def send_email_with_pdf(recipient_email, generated_text):
    pdf_output = generate_pdf(generated_text)
    msg = Message("Your Generated Text", recipients=[recipient_email])
    msg.body = "Here is the PDF containing your generated text."
    msg.attach("generated_text.pdf", "application/pdf", pdf_output.read())
    try:
        current_app.extensions['mail'].send(msg)
        return True
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return False

# Route to handle Tally form submission
@text_generation_bp.route("/generate-text", methods=["POST"])
def generate_text():
    try:
        prompt = request.form.get("prompt")
        email = request.form.get("email")
        if not prompt or not email:
            return {"error": "Prompt and email are required."}, 400

        # Generate text
        generated_text = generate_long_text(prompt)

        # Send generated text as a PDF
        if send_email_with_pdf(email, generated_text):
            return render_template("success.html", email=email)
        else:
            return {"error": "Failed to send email."}, 500
    except Exception as e:
        logging.error(f"Error during text generation: {e}")
        return {"error": str(e)}, 500

@text_generation_bp.route("/")
def home():
    return render_template("home.html")





