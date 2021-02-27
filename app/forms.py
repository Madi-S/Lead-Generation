from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class UserRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(4, 100, 'First name should consist of 4-200 characters')])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(4, 100, 'Last name should consist of 4-200 characters')])
    username = StringField('Username (4-30)', validators=[DataRequired(), Length(4, 30, 'Username should consist of 4-30 characters')])
    password = PasswordField('Password (6-40)', validators=[DataRequired(), Length(6, 40, 'Passowrd should consist of 6-40 characters')])
    recaptcha = RecaptchaField()


class UserLoginForm(FlaskForm):
    username = StringField('Username (4-30)', validators=[DataRequired(), Length(4, 30, 'Username should consist of 4-30 characters')])
    password = StringField('Password (6-40)', validators=[DataRequired(), Length(6, 40, 'Passowrd should consist of 6-40 characters')])
    
    submit = SubmitField('Register')
    