from flask import Flask, request, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import (StringField,
                      PasswordField,
                        SubmitField,
                          EmailField,
                            ValidationError,
                              RadioField,
                                SelectField,
                                TelField,
                                DateField)
from wtforms.validators import DataRequired, Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'superduperupersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    
    profile = db.relationship('UserPersonalData', back_populates='user', uselist=False) # uselist one-to-one užtikrina

    def __repr__(self):
        return f'<User {self.email}>'
    
class UserPersonalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    phone_number =  db.Column(db.Integer, unique=True)
    gender = db.Column(db.String(10), nullable=True)
    
    user = db.relationship('User', back_populates='profile')
    

class CustomPasswordValidator(object):
    def __init__(self):
        self.message = 'Password must have at least one upper letter and at least one symbol and at least one number and no space'

    def __call__(self, form, field):
        text : str = field.data
        is_any_numbers = any(x.isdigit() for x in text)
        is_any_upper = any(x.isupper() for x in text)
        is_any_symbol = any(not x.isalnum() for x in text)
        is_any_space = any(x.isspace() for x in text)

        if not (is_any_numbers and is_any_upper and is_any_symbol) or is_any_space:
            raise ValidationError(self.message)

class RegisterForm(FlaskForm):
    email =  EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(8,20), CustomPasswordValidator()])

    submit = SubmitField("Submit")


class RegisterForm_2(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    date_of_birth = DateField('Date of birth', validators=[InputRequired()])
    country = SelectField('Country', choices=[('LT', 'Lithuania'), ('US', 'United States'),
                                              ('ESP', 'Spain')])
    phone_number = TelField('Phone number', validators=[InputRequired()])
    gender = RadioField('Gender', choices=[
                        ('male', 'Male'), ('female', 'Female')])
    
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
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

        return redirect(url_for('register_2'))
    return render_template('register.html', form=form)

@app.route('/register/step2', methods=['GET', 'POST'])
def register_2():
    form = RegisterForm_2()

    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('register'))  # Prevent orphan profile creation

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            return 'Logged in successful!'
        else:
            form.password.errors.append('Invalid email or password')
    return render_template('login.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
