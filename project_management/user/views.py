from flask import render_template,Blueprint,flash,redirect,url_for
from project_management.user.forms import LoginForm,RegistrationForm
from project_management.models import User
from project_management import db
from werkzeug.security import generate_password_hash
from flask_login import logout_user,login_user,login_required,current_user
user=Blueprint('user',__name__)

@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_mail = form.user_mail.data
        password = form.password.data

        user = User.query.filter_by(user_mail=user_mail).first()
        if user and user.check_password(password):
            flash('Login successful!', 'success')
            login_user(user)
            return redirect(url_for('core.index'))

        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', form=form,current_user=current_user)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('user.login'))
@user.route('/register', methods=['GET', 'POST'])
def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            username = form.username.data
            user_mail = form.user_mail.data
            password = form.password.data
            existing_user = User.query.filter_by(user_mail=user_mail).first()
            if existing_user:
                flash('Email already registered.', 'danger')
                return redirect(url_for('user.register'))

            new_user = User(username=username, user_mail=user_mail, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('user.login'))

        return render_template('register.html', form=form,current_user=current_user)