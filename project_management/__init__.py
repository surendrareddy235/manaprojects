from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import base64
from markupsafe import Markup
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')

# SQLite DB config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'


from project_management.user.views import user
from project_management.core.views import core
from project_management.projects.views import project
from project_management.email.views import email
app.register_blueprint(email)
app.register_blueprint(project)
app.register_blueprint(user)
app.register_blueprint(core)
@app.template_filter('b64encode')
def b64encode_filter(binary):
    return Markup(base64.b64encode(binary).decode('utf-8'))
