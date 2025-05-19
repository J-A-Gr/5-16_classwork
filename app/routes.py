from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, render_template, url_for, redirect, session, Blueprint
from app.forms import RegisterForm, RegisterForm_2, LoginForm
from app.models import User, UserPersonalData
from app import db
from app import create_app

routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    return render_template('index.html')


@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if email already exists
        if User.query.filter_by(email=form.email.data).first():
            form.email.errors.append("This email is already in use.")
            return render_template('register.html', form=form)
        
        new_user = User(
            email=form.email.data,
            password=generate_password_hash(form.password.data)
            )
        db.session.add(new_user)
        db.session.commit()
        # Store user_id in session
        session['user_id'] = new_user.id

        return redirect(url_for('routes.register_2'))
    return render_template('register.html', form=form)

@routes.route('/register/step2', methods=['GET', 'POST'])
def register_2():
    form = RegisterForm_2()

    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('routes.register'))  # Prevent orphan profile creation

    if form.validate_on_submit():
        new_data = UserPersonalData(
            user_id=user_id,
            name=form.name.data,
            date_of_birth=form.date_of_birth.data,
            country=form.country.data,
            phone_number=form.phone_number.data,
            gender=form.gender.data
        )
        db.session.add(new_data)
        db.session.commit()

        session.pop('user_id') # Clean up session after use

        return "Registration Successful!"
    return render_template('register2.html', form=form)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            return 'Logged in successful!'
        else:
            form.password.errors.append('Invalid email or password')
    return render_template('login.html', form=form)

