from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField, DateField, BooleanField, IntegerField, TimeField, SelectField, TextAreaField, FloatField, FieldList, FormField, SelectMultipleField
from wtforms.validators import InputRequired, ValidationError, Length, Email, EqualTo, DataRequired, Optional
from flask_bootstrap import Bootstrap

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
    mode_of_transport = [('Pet Owner Deliver', 'Pet Owner Deliver'), ('Care Taker Pick Up', 'Care Taker Pick Up'),
                        ('Transfer through PCS Building', 'Transfer through PCS Building'), ('N.A', 'N.A')]
    mode_of_payment = [('1', 'Credit Card'), ('2', 'Cash'), ('3', 'N.A')]
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
    mode_of_transport = SelectField('If you have chosen to sign up as a Care Taker, How do you prefer the pet you will take care of to be transported? Select N.A if you are signing up as a pet owner',
                                    choices=mode_of_transport)
    mode_of_payment = SelectField('If you have chosen to sign up as a Care Taker, select how your prefer mode of payment from pet owners. Select N.A if you are signing up as a pet owner',
                                    choices=mode_of_payment)
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
                ('Hamster', 'Hamster'), ('Fish', 'Fish'),
                ('Mice', 'Mice'), ('Terrapin', 'Terrapin'), ('Bird', 'Bird')]
    pet_name = StringField('Pet Name', validators=[DataRequired()])
    category = SelectField('What is the category of your pet?', choices=categories)
    age = IntegerField('How old is your pet?', validators=[DataRequired()])
    special_care1 = StringField('Write down special considerations that your pet if there is any, else leave this blank', validators=[Optional()])
    special_care2 = StringField('Write down special considerations that your pet if there is any, else leave this blank', validators=[Optional()])
    special_care3 = StringField('Write down special considerations that your pet if there is any, else leave this blank', validators=[Optional()])
    #special_care = FieldList(FormField(SpecialCareForm), min_entries=5, validators=[Optional()])
    submit = SubmitField('Register Pet')


class PartTimeSetPriceForm(FlaskForm):
    categories = [('Dog', 'Dog'), ('Cat', 'Cat'), ('Rabbit', 'Rabbit'),
                ('Hamster', 'Hamster'), ('Fish', 'Fish'), ('Guinea Pig', 'Guinea Pig'),
                ('Mice', 'Mice'), ('Terrapin', 'Terrapin'), ('Bird', 'Bird')]
    #pet_type_choice = SelectMultipleField('Choose the type of pets you want to take care of', choices=categories)
    Dog = IntegerField('Dog', validators=[Optional()])
    Cat = IntegerField('Cat', validators=[Optional()])
    Rabbit = IntegerField('Rabbit', validators=[Optional()])
    Hamster = IntegerField('Hamster', validators=[Optional()])
    Fish = IntegerField('Fish', validators=[Optional()])
    Mice = IntegerField('Mice', validators=[Optional()])
    Terrapin = IntegerField('Terrapin', validators=[Optional()])
    Bird = IntegerField('Bird', validators=[Optional()])
    submit = SubmitField('Set Prices')

class FullTimeChoosePetTypeForm(FlaskForm):
    choice = [('Yes','Yes'),('No','No')]
    Dog = SelectField('Dog',choices=choice)
    Cat = SelectField('Cat',choices=choice)
    Rabbit = SelectField('Rabbit',choices=choice)
    Hamster = SelectField('Hamster',choices=choice)
    Fish = SelectField('Fish',choices=choice)
    Mice = SelectField('Mice',choices=choice)
    Terrapin = SelectField('Terrapin',choices=choice)
    Bird = SelectField('Bird',choices=choice)
    submit = SubmitField('Choose pet types!')

class TestForm(FlaskForm):
    date = DateField('Pick a Date', format="%m/%d/%Y")
    submit = SubmitField('Choose pet types!')

class SearchCareTakerForm(FlaskForm):
    employment = [('1', 'Part Time'), ('2', 'Full Time')]
    ratings = [('0', '0'), ('1', '1'), ('2','2'),('3','3'),('4','4'),('5','5')]
    categories = [('Dog', 'Dog'), ('Cat', 'Cat'), ('Rabbit', 'Rabbit'),
                ('Hamster', 'Hamster'), ('Fish', 'Fish'),
                ('Mice', 'Mice'), ('Terrapin', 'Terrapin'), ('Bird', 'Bird')]
    mode_of_transport = [('Pet Owner Deliver', 'Pet Owner Deliver'), ('Care Taker Pick Up', 'Care Taker Pick Up'),
                        ('Transfer through PCS Building', 'Transfer through PCS Building')]
    mode_of_payment = [('Credit Card', 'Credit Card'), ('Cash', 'Cash')]
    employment_type = SelectField('Employment', choices=employment)
    category = SelectField('Pet Type', choices=categories)
    rating = SelectField('Rating', choices=ratings)
    preferred_mode_of_transport = SelectField('Preferred Mode of Transport of Pet', choices=mode_of_transport)
    preferred_mode_of_payment = SelectField('Preferred Mode of Payment to the Care Taker', choices=mode_of_payment)
    startDate = DateField('Start date',validators=[InputRequired()],format='%Y-%m-%d')
    endDate = DateField('End date',validators=[InputRequired()],format='%Y-%m-%d')
    submit = SubmitField('Search Caretaker')

class UpdateAvailabilityForm(FlaskForm):
    leaveDate = DateField('Date to take leave',validators=[InputRequired()],format='%Y-%m-%d')
    submit = SubmitField('Update Availability!')
