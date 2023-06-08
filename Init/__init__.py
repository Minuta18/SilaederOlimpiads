from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from . import config

app = Flask('Main')
app.config.from_object(config)

db = SQLAlchemy(app)

login_manager = LoginManager()
# login_manager.login_view = 'login'
login_manager.init_app(app)