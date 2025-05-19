from flask_wtf import FlaskForm
from wtforms import (StringField,
                      PasswordField,
                        SubmitField,
                          EmailField,
                              RadioField,
                                SelectField,
                                TelField,
                                DateField)
from wtforms.validators import DataRequired, Email, Length, InputRequired
from app.validators import CustomPasswordValidator

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