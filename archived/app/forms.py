from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, BooleanField, Form
from wtforms.validators import DataRequired, Length, EqualTo


class UserRegistrationForm(FlaskForm):
    first_name = StringField('First Name', [DataRequired(), Length(
        4, 100, 'First name should consist of 4-200 characters')])
    last_name = StringField('Last Name', [DataRequired(), Length(
        4, 100, 'Last name should consist of 4-200 characters')])
    username = StringField('Username (4-30)', [DataRequired(), Length(
        4, 30, 'Username should consist of 4-30 characters')])
    password = PasswordField(
        'Password (6-40)', [DataRequired(), Length(6, 40, 'Passowrd should consist of 6-40 characters')])
    repeat_password = PasswordField('Repeat Password')
    accept_terms = BooleanField('I accept the TOS', [DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')

    @property
    def visible_fields(self):
        return (self.first_name, self.last_name, self.username, self.password, self.repeat_password)


class UserLoginForm(FlaskForm):
    username = StringField('Username (4-30)', validators=[DataRequired(), Length(
        4, 30, 'Username should consist of 4-30 characters')])
    password = PasswordField('Password (6-40)', validators=[DataRequired(), Length(
        6, 40, 'Passowrd should consist of 6-40 characters')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Sign In')

    @property
    def visible_fields(self):
        return (self.username, self.password)
