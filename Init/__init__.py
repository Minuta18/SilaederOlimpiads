from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from flask_mail import Mail
import smtplib as smtp
from . import config

app = Flask('Main')
app.config.from_object(config)

# mail = Mail(app)
# self_email = config.MAIL_USERNAME

db = SQLAlchemy(app)

login_manager = LoginManager()
# login_manager.login_view = 'login'
login_manager.init_app(app)