import smtplib
from email.mime.text import MIMEText
from email.header import Header
from flask import current_app

def send_phishing_email(to_address, subject, body, tracking_link):
    """
    Sends a phishing email with a tracking link.
    """
    msg = MIMEText(body.replace("{{tracking_link}}", tracking_link), 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = current_app.config['SMTP_FROM_ADDRESS']
    msg['To'] = to_address

    try:
        with smtplib.SMTP(current_app.config['SMTP_SERVER'], current_app.config['SMTP_PORT']) as server:
            server.starttls()  # Upgrade to a secure TLS connection
            server.login(current_app.config['SMTP_USERNAME'], current_app.config['SMTP_PASSWORD'])
            server.send_message(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email to {to_address}: {e}")
        return False