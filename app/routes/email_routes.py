import os

from flask import Flask, Blueprint, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

email_bp = Blueprint('email_bp', __name__)


@email_bp.route('/send-email', methods=['POST'])
def send_email():
    data = request.json  # Assuming JSON data is sent from Vue.js
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', 587))

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'New Contact Form Submission'

    body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)  # Replace with SMTP server details
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return jsonify({'error': str(e)}), 500


app.register_blueprint(email_bp, url_prefix='/email')
