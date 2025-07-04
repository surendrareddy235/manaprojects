from flask import  render_template, flash, redirect, url_for,Blueprint,request
from flask_mail import Mail, Message
from  project_management.email.forms import ContactForm
from project_management import app
from project_management.models import Email
from project_management import db
from flask_login import login_required
from dotenv import load_dotenv
import os
load_dotenv()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)
email=Blueprint('email',__name__)



@email.route('/contact', methods=['GET', 'POST'])
def contact_form():
    form = ContactForm()
    if form.validate_on_submit():
        # ✅ Store in DB (update field names to match model)
        contact_msg = Email(
            user_name=form.name.data,
            user_email=form.email.data,
            user_mobile=form.mobile.data,
            email_subject=form.subject.data,
            email_query=form.query.data
        )
        db.session.add(contact_msg)
        db.session.commit()

        # ✅ Send email
        msg = Message(
            subject=form.subject.data,
            sender=form.email.data,
            recipients=[os.getenv('MAIL_USERNAME')],
            body=(
                f"Name:   {form.name.data}\n"
                f"Email:  {form.email.data}\n"
                f"Mobile: {form.mobile.data}\n\n"
                f"Message:\n{form.query.data}"
            )
        )
        try:
            mail.send(msg)
            return redirect(url_for('email.contact_form', success='1'))
        except Exception as e:
            return redirect(url_for('email.contact_form', error=str(e)))

    success = request.args.get('success')
    error = request.args.get('error', '')
    return render_template('form.html', form=form, success=success, error=error)

@email.route('/all_contacts')
@login_required  # Optional: Only allow logged-in users (e.g., admin) to see messages
def all_contacts():
    all_messages = Email.query.order_by(Email.user_id.desc()).all()
    return render_template('emails.html', messages=all_messages)