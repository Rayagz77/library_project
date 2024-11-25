# controllers/text_generation_controller.py

from flask import Blueprint, request, render_template, current_app, send_file
from fpdf import FPDF
import requests
from flask_mail import Message, Mail
import os
from io import BytesIO

# Create the blueprint for text generation
text_generation_bp = Blueprint('text_generation', __name__)

# Initialize Flask-Mail
mail = Mail()

# Function to generate a long text using Hugging Face API
def generate_long_text(prompt, min_tokens=1500, max_tokens=3000):
    url = "https://api-inference.huggingface.co/models/gpt-2"  # Example using GPT-2 model
    headers = {
        "Authorization": f"Bearer {current_app.config['HUGGINGFACE_API_KEY']}"
    }
    
    # Make the request to Hugging Face
    response = requests.post(url, headers=headers, json={
        "inputs": prompt,
        "max_length": max_tokens
    })
    
    result = response.json()
    
    if 'choices' in result:
        return result['choices'][0]['text']
    else:
        return "Error generating the text."

# Function to generate PDF from the text
def generate_pdf(text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add the text content to the PDF
    pdf.multi_cell(0, 10, text)
    
    # Save to a BytesIO stream
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    
    return pdf_output

# Function to send the email with the PDF attached
def send_email_with_pdf(recipient_email, generated_text):
    # Generate the PDF from the text
    pdf_output = generate_pdf(generated_text)
    
    # Send the email
    msg = Message("Your Generated Text as PDF", recipients=[recipient_email])
    msg.body = "Attached is the PDF containing your generated text."
    msg.attach("generated_text.pdf", "application/pdf", pdf_output.read())

    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    
    return True

# Function to notify the admin via email
def notify_admin_admin(generated_text):
    admin_email = "admin_email@example.com"  # Replace with actual admin email
    subject = "Text Generation Completed"
    body = f"A new text has been generated successfully. Text preview: {generated_text[:100]}..."
    
    msg = Message(subject, recipients=[admin_email])
    msg.body = body
    
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error sending admin notification: {e}")
        return False
    
    return True

# controllers/text_generation_controller.py

@text_generation_bp.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get the prompt from the form (Tally form integrated)
        prompt = request.form.get("tally_prompt")
        
        # Generate the text based on the prompt
        generated_text = generate_long_text(prompt)
        
        # Send the email to the user with the PDF
        user_email = request.form.get("user_email")  # User's email from the form
        if send_email_with_pdf(user_email, generated_text):
            print(f"PDF sent successfully to {user_email}")
        
        # Notify the admin that the operation has been completed
        notify_admin_admin(generated_text)
        
        return render_template("home.html", generated_text=generated_text, tally_prompt=prompt)
    
    return render_template("home.html", generated_text=None, tally_prompt=None)

