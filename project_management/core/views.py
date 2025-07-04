from flask import  Blueprint,render_template
from project_management.models import Project
from flask_login import  login_required

core=Blueprint('core',__name__)
import base64
@core.route('/')
def index():
    projects = Project.query.all()  # fetch all projects from the database
    return render_template('index.html', projects=projects)
@core.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@core.route("/project/<int:project_id>")
def project(project_id):
    project_obj = Project.query.get_or_404(project_id)
    return render_template("project.html", project=project_obj)

