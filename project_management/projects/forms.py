from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, FileField,SubmitField
from wtforms.validators import DataRequired,Length
from flask_wtf.file import FileAllowed

class ProjectForm(FlaskForm):
    project_name = StringField("Project Name", validators=[DataRequired()])
    project_description = TextAreaField("Description", validators=[DataRequired()])
    project_price = FloatField("Price", validators=[DataRequired()])
    project_technologies = StringField("Technologies", validators=[DataRequired()])

    # File Uploads
    project_thumbnail = FileField("Thumbnail", validators=[FileAllowed(["jpg", "png", "jpeg",'webp'])])
    project_image_1 = FileField("Image 1", validators=[FileAllowed(["jpg", "png", "jpeg",'webp'])])
    project_image_2 = FileField("Image 2", validators=[FileAllowed(["jpg", "png", "jpeg",'webp'])])
    project_image_3 = FileField("Image 3", validators=[FileAllowed(["jpg", "png", "jpeg",'webp'])])
    project_image_4 = FileField("Image 4", validators=[FileAllowed(["jpg", "png", "jpeg",'webp'])])
    project_image_5 = FileField("Image 5", validators=[FileAllowed(["jpg", "png", "jpeg",'webp'])])
    project_file = FileField("Project File", validators=[FileAllowed(["zip", "pdf", "docx", "pptx", "rar"])])
    submit = SubmitField("Create Project")
# project_management/projects/forms.py

class EditProjectForm(FlaskForm):
    project_name = StringField("Project Name", validators=[
        DataRequired(), Length(min=2, max=100)
    ])

    project_description = StringField("Description", validators=[
        DataRequired(), Length(min=5, max=500)
    ])

    project_price = FloatField("Price (INR)", validators=[DataRequired()])

    project_technologies = StringField("Technologies (comma-separated)", validators=[
        DataRequired(), Length(min=2)
    ])

    project_thumbnail = FileField("Thumbnail", validators=[
        FileAllowed(['jpg', 'jpeg', 'png','webp'], "Images only!")
    ])

    project_image_1 = FileField("Gallery Image 1", validators=[
        FileAllowed(['jpg', 'jpeg', 'png','webp'], "Images only!")
    ])
    project_image_2 = FileField("Gallery Image 2", validators=[
        FileAllowed(['jpg', 'jpeg', 'png','webp'], "Images only!")
    ])
    project_image_3 = FileField("Gallery Image 3", validators=[
        FileAllowed(['jpg', 'jpeg', 'png','webp'], "Images only!")
    ])
    project_image_4 = FileField("Gallery Image 4", validators=[
        FileAllowed(['jpg', 'jpeg', 'png','webp'], "Images only!")
    ])
    project_image_5 = FileField("Gallery Image 5", validators=[
        FileAllowed(['jpg', 'jpeg', 'png','webp'], "Images only!")
    ])

    project_file = FileField("Supporting File (PDF/ZIP/DOCX/etc.)", validators=[
        FileAllowed(['pdf', 'zip', 'docx', 'txt'], "Valid file formats only!")
    ])

    submit = SubmitField("Update Project")
