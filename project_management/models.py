from werkzeug.security import generate_password_hash, check_password_hash
from project_management import db, login_manager
from flask_login import UserMixin

# ---------- Flask-Login Loader ----------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# ---------- Table 1: Users ----------
class User(db.Model, UserMixin):
    __tablename__ = "user"
    user_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    user_mail = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    def __init__(self, username, user_mail, password):
        self.username = username
        self.user_mail = user_mail
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return f"<User {self.username}>"

# ---------- Table 2: Projects ----------
class Project(db.Model):
    __tablename__ = "projects"
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(150), nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    project_price = db.Column(db.Float, nullable=False)
    project_technologies = db.Column(db.String(256), nullable=False)
    project_thumbnail = db.Column(db.LargeBinary(length=(16 * 1024 * 1024)), nullable=True)  # 16MB
    project_image_1 = db.Column(db.LargeBinary(length=(16 * 1024 * 1024)), nullable=True)  # 16MB
    project_image_2 = db.Column(db.LargeBinary(length=(16 * 1024 * 1024)), nullable=True)  # 16MB
    project_image_3= db.Column(db.LargeBinary(length=(16 * 1024 * 1024)), nullable=True)  # 16MB
    project_image_4 = db.Column(db.LargeBinary(length=(16 * 1024 * 1024)), nullable=True)  # 16MB
    project_image_5= db.Column(db.LargeBinary(length=(16 * 1024 * 1024)), nullable=True)  # 16MB
    project_file = db.Column(db.LargeBinary(length=(64 * 1024 * 1024)), nullable=True)  # 64MB
    project_file_name = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Project {self.project_name}>"

class Email(db.Model):
    __tablename__='email'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name=db.Column(db.String(255), nullable=False)
    user_email=db.Column(db.String(255), nullable=False)
    user_mobile=db.Column(db.String(255), nullable=False)
    email_subject=db.Column(db.Text, nullable=True)
    email_query=db.Column(db.Text, nullable=True)