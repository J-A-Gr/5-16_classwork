from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, ValidationError
from wtforms.validators import DataRequired, Email, Length


app = Flask(__name__)
app.config['SECRET_KEY'] = 'superduperupersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

class CustomPasswordValidator(object):
    def __init__(self):
        self.message = 'Password must have at least one upper letter and at least one symbol and at least one number and no space'

    def __call__(self, form, field):
        text : str = field.data
        is_any_numbers = any(filter(lambda x: x.isdigit(), text))
        is_any_upper = any(filter(lambda x: x.isupper(), text)) 
        is_any_symbol = any(filter(lambda x: x.isalnum(), text))
        is_any_space = any(filter(lambda x: x == ' ', text))
        if is_any_numbers is False or is_any_upper is False or is_any_symbol is False or is_any_space is True:
            raise ValidationError(self.message)

class RegisterForm(FlaskForm):
    email =  EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(8,20), CustomPasswordValidator()])

    submit = SubmitField("Register")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            password=form.password.data
            )
        db.session.add(new_user)
        db.session.commit()
        return 'Registration successful!'
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            return 'Logged in successful!'
        else:
            return 'Invalid email or password. (Check if user with provided email and password exists)'
    return render_template('login.html', form=form)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
