import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if os.environ.get('SQLALCHEMY_DATABASE_URI'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_PASSWORD= os.environ.get('EMAIL_PASS')
    MAIL_USERNAME = os.environ.get('EMAIL_USER')