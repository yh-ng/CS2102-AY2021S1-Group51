from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField, DateField, BooleanField, IntegerField, TimeField, SelectField, TextAreaField, FloatField, FieldList, FormField
from wtforms.validators import InputRequired, ValidationError, Length, Email, EqualTo, DataRequired, Optional

def is_valid_name(form, field):
    if not all(map(lambda char: char.isalpha(), field.data)):
        raise ValidationError('This field should only contain alphabets')


def agrees_terms_and_conditions(form, field):
    if not field.data:
        raise ValidationError('You must agree to the terms and conditions to sign up')


class RegistrationForm(FlaskForm):
    gender = [('Male', 'Male'), ('Female', 'Female')]
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
    gender = SelectField('Select your gender.', choices=gender)
    area = SelectField('Which area do you stay at?', choices=areachoice)
    select1 = SelectField('What do you want to sign up as?', choices=choice1)
    select2 = SelectField('If you have chosen to sign up as a Care Taker, do you want to work part time or full time?', choices=choice2)
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    ##email = StringField('Email',
    ##                    validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SpecialCareForm(FlaskForm):
    specialcare = StringField('Special Care', validators=[Optional()])

class PetRegistrationForm(FlaskForm):
    categories = [('Dog', 'Dog'), ('Cat', 'Cat'), ('Rabbit', 'Rabbit'),
                ('Hamster', 'Hamster'), ('Fish', 'Fish'), ('Guinea Pig', 'Guinea Pig'),
                ('Mice', 'Mice'), ('Terrapin', 'Terrapin'), ('Bird', 'Bird')]
    pet_name = StringField('Pet Name', validators=[DataRequired()])
    category = SelectField('What is the category of your pet?', choices=categories)
    age = IntegerField('How old is your pet?', validators=[DataRequired()])
    special_care1 = StringField('Write down special considerations that your pet if there is any, else leave this blank', validators=[Optional()])
    special_care2 = StringField('Write down special considerations that your pet if there is any, else leave this blank', validators=[Optional()])
    special_care3 = StringField('Write down special considerations that your pet if there is any, else leave this blank', validators=[Optional()])
    #special_care = FieldList(FormField(SpecialCareForm), min_entries=5, validators=[Optional()])
    submit = SubmitField('Register Pet')
