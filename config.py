import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_for_development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SMTP Configuration (PLACEHOLDER VALUES - CHANGE THESE!)
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587  # Or 465 for SSL
    SMTP_USERNAME = '' #Your Username to be shown in the mail
    SMTP_PASSWORD = '' #Your app's mail address refer to the Readme.me for more details
    SMTP_FROM_ADDRESS = '' #Anything mostly like a mail address for I don't know why
