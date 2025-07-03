from flask import (
    Blueprint, render_template, redirect, url_for,
    flash,  abort
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from flask import send_file
import io
import base64
from project_management import db
from project_management.projects.forms import ProjectForm,EditProjectForm
from project_management.models import Project

project = Blueprint("project", __name__)

@project.route("/project/create", methods=["GET", "POST"])
@login_required
def create_project():
    form = ProjectForm()

    if form.validate_on_submit():
        # Process uploaded files
        thumbnail_data = form.project_thumbnail.data.read() if form.project_thumbnail.data else None
        image_1 = form.project_image_1.data.read() if form.project_image_1.data else None
        image_2 = form.project_image_2.data.read() if form.project_image_2.data else None
        image_3 = form.project_image_3.data.read() if form.project_image_3.data else None
        image_4 = form.project_image_4.data.read() if form.project_image_4.data else None
        image_5 = form.project_image_5.data.read() if form.project_image_5.data else None

        project_file = form.project_file.data
        file_data = project_file.read() if project_file else None
        file_name = secure_filename(project_file.filename) if project_file else None

        # Create the new project
        new_project = Project(
            project_name=form.project_name.data,
            project_description=form.project_description.data,
            project_price=form.project_price.data,
            project_technologies=form.project_technologies.data,
            project_thumbnail=thumbnail_data,
            project_image_1=image_1,
            project_image_2=image_2,
            project_image_3=image_3,
            project_image_4=image_4,
            project_image_5=image_5,
            project_file=file_data,
            project_file_name=file_name,
        )

        db.session.add(new_project)
        db.session.commit()
        flash("Project created successfully!", "success")
        return redirect(url_for("project.projects"))

    return render_template("create_project.html", form=form)

@project.route("/projects")
def projects():
    all_projects = Project.query.all()
    return render_template("projects.html", projects=all_projects)

@project.route("/view_project/<int:project_id>")
def view_project(project_id):
    project_obj = Project.query.get_or_404(project_id)
    return render_template("view_project.html", project=project_obj)



@project.route('/projects/<int:project_id>/download', methods=['GET'])
@login_required
def download_file(project_id):
    project_obj = Project.query.get_or_404(project_id)

    if not project_obj.project_file or not project_obj.project_file_name:
        flash('No file found for this project.', 'warning')
        return redirect(url_for('project.view_project', project_id=project_id))

    # Assuming you store file as BLOB or base64 in project.project_file
    file_data = base64.b64decode(project_obj.project_file)
    return send_file(
        io.BytesIO(file_data),
        as_attachment=True,
        download_name=project_obj.project_file_name
    )
@project.route("/project/<int:project_id>/delete", methods=["POST"])
@login_required
def delete_project(project_id: int):
    proj = Project.query.get_or_404(project_id)

    # ---- authorization ----------------------------------------------------
    if proj.user_id != current_user.user_id:
        abort(403, description="You are not authorized to delete this project.")

    # ---- delete children (only needed if you did NOT add cascade on rels) --
    for img in proj.images:
        db.session.delete(img)
    for f in proj.files:
        db.session.delete(f)

    # ---- delete parent project -------------------------------------------
    db.session.delete(proj)
    db.session.commit()

    flash("Project deleted successfully!", "success")
    return redirect(url_for("project.projects"))


@project.route('/project/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project_obj = Project.query.get_or_404(project_id)



    form = EditProjectForm(obj=project_obj)

    if form.validate_on_submit():
        project_obj.project_name         = form.project_name.data
        project_obj.project_description  = form.project_description.data
        project_obj.project_price        = float(form.project_price.data)
        project_obj.project_technologies = form.project_technologies.data

        # Thumbnail upload
        if form.project_thumbnail.data:
            if hasattr(form.project_thumbnail.data, 'read'):
                project_obj.project_thumbnail = form.project_thumbnail.data.read()
            else:
                project_obj.project_thumbnail = form.project_thumbnail.data

        # Gallery images (project_image_1 to project_image_5)
        for i in range(1, 6):
            field = getattr(form, f'project_image_{i}')
            if field.data:
                if hasattr(field.data, 'read'):
                    setattr(project_obj, f'project_image_{i}', field.data.read())
                else:
                    setattr(project_obj, f'project_image_{i}', field.data)

        # Project file (single file + name)
        if form.project_file.data:
            if hasattr(form.project_file.data, 'read'):
                project_obj.project_file = form.project_file.data.read()
                project_obj.project_file_name = form.project_file.data.filename
            else:
                project_obj.project_file = form.project_file.data
                project_obj.project_file_name = form.project_file.data.filename if hasattr(form.project_file.data, 'filename') else None

        db.session.commit()
        flash('Project updated.', 'success')
        return redirect(url_for('project.view_project', project_id=project_id))

    return render_template('edit_project.html', form=form, project=project_obj)

