from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import InputRequired, ValidationError, Length, Email, EqualTo, DataRequired, InputRequired

def is_valid_name(form, field):
    if not all(map(lambda char: char.isalpha(), field.data)):
        raise ValidationError('This field should only contain alphabets')


def agrees_terms_and_conditions(form, field):
    if not field.data:
        raise ValidationError('You must agree to the terms and conditions to sign up')


class RegistrationForm(FlaskForm):
    choice1 = [('1', 'Pet Owner'), ('2', 'Care Taker'), ('3', 'Both')]
    choice2 = [('1', 'Part Time'), ('2', 'Full Time'), ('3', 'N.A')]
    areachoice = [('North', 'North'), ('East', 'East'), ('South', 'South'), ('West', 'West'), ('Central', 'Central')]
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    area = SelectField('Which area do you stay at?', choices=areachoice)
    select1 = SelectField('What do you want to be?', choices=choice1)
    select2 = SelectField('Part time or full time?', choices=choice2)
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    ##email = StringField('Email',
    ##                    validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
