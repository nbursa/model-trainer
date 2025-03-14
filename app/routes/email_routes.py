import os
import smtplib
import ssl
import logging
import time
from threading import Thread
from flask import Blueprint, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Define Flask Blueprint
email_bp = Blueprint('email_bp', __name__)

def get_env_variable(var_name, default=None):
    """Helper function to get environment variables with default values."""
    value = os.getenv(var_name, default)
    if value is None:
        logger.warning(f"⚠️ Missing environment variable: {var_name}")
    return value

# Load SMTP configurations
SENDER_EMAIL = get_env_variable('SENDER_EMAIL')
RECEIVER_EMAIL = get_env_variable('RECEIVER_EMAIL')
EMAIL_PASSWORD = get_env_variable('EMAIL_PASSWORD')
SMTP_SERVER = get_env_variable('SMTP_SERVER')
SMTP_PORT = int(get_env_variable('SMTP_PORT'))

def send_email_async(name, email, message, is_support=False):
    """Send email asynchronously in a background thread."""
    def send():
        subject = "Support Request" if is_support else "New Contact Form Submission"
        recipient = RECEIVER_EMAIL if not is_support else get_env_variable('SUPPORT_EMAIL', RECEIVER_EMAIL)

        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(f"Name: {name}\nEmail: {email}\nMessage:\n{message}", 'plain'))

        attempt = 0
        max_retries = 3

        while attempt < max_retries:
            try:
                logger.info(f"📨 Sending email (Attempt {attempt + 1}) to {recipient}...")

                # ✅ Use SSL for Port 465
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
                    server.login(SENDER_EMAIL, EMAIL_PASSWORD)
                    server.sendmail(SENDER_EMAIL, recipient, msg.as_string())

                logger.info(f"✅ Email successfully sent to {recipient}")
                return {'message': 'Email sent successfully'}
            except Exception as e:
                logger.error(f"❌ Email sending failed (Attempt {attempt + 1}): {e}")
                time.sleep(2)
                attempt += 1

        logger.error("🚨 Failed to send email after multiple attempts")
        return {'error': 'Failed to send email after multiple attempts'}

    # Run email sending in a separate thread
    thread = Thread(target=send)
    thread.start()

@email_bp.route('/send-email', methods=['POST'])
def send_email():
    """API Endpoint for users to contact the system administrator."""
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not all([name, email, message]):
            return jsonify({'error': 'Missing required fields'}), 400

        response = send_email_async(name, email, message)

        return jsonify({'message': 'Email is being sent in the background'}), 200

    except Exception as e:
        logger.error(f"❌ Unexpected error in /send-email: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@email_bp.route('/support', methods=['POST'])
def report_issue():
    """API Endpoint for users to report issues (Contact Support)."""
    try:
        data = request.json
        name = data.get('name', 'Unknown User')
        email = data.get('email', 'N/A')
        issue = data.get('issue')

        if not issue:
            return jsonify({'error': 'Issue description is required'}), 400

        # Log issue to a local file for debugging
        with open("support_issues.log", "a") as log_file:
            log_file.write(f"User: {name} ({email}) | Issue: {issue}\n")

        # Send an email to support team
        response = send_email_async(name, email, issue, is_support=True)

        return jsonify({'message': 'Support request is being sent'}), 200

    except Exception as e:
        logger.error(f"❌ Unexpected error in /support: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
