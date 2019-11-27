from datetime import datetime
from flask import Flask
from flask_login import LoginManager
from models import db

application = Flask(__name__)
application.config.from_object("config.BaseConfig")

db.init_app(application)

login_manager = LoginManager(application)
login_manager.login_view = "login"
login_manager.login_message = "Para aceder a esta funcionalidade, deve em primeiro lugar autenticar-se."
login_manager.login_message_category = "warning"

# All views (it must be in this position)
from views import *

if __name__ == "__main__":
    application.run(debug=True)
