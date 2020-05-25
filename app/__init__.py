from flask import Flask

app=Flask(__name__)

from app import queries

from app import routes
from flask_login import LoginManager

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

