from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject=StringField('Subject' ,validators=[DataRequired()])
    query = TextAreaField('Query', validators=[DataRequired(), Length(min=10, max=1000)])
    mobile=StringField('Mobile',validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Submit Query')
