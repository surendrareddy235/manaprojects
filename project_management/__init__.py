from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import base64
from markupsafe import Markup
app = Flask(__name__)
app.secret_key = 'surendra'

# SQLite DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Thanmay047%40@localhost/projects'
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
