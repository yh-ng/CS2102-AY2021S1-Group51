from flask import Blueprint, redirect, render_template, flash, url_for, request
from flask_login import current_user, login_required, login_user, UserMixin, logout_user


from __init__ import db, login_manager
from forms import *
from tables import *
from models import Users

import psycopg2
import psycopg2.extras
import math

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect

view = Blueprint("view", __name__)


@login_manager.user_loader
def load_user(username):
    user = Users.query.filter_by(username=username).first()
    return user or current_user

##############################
# Can get away using the below 3 functions for now, but it would be better to find a better method
# to obtain what is the role of the user to restrict and give access selected pages to him
def is_user_a_petowner(current_user):
    query = "SELECT * FROM PetOwners WHERE username = '{}'".format(current_user.username)
    exists_user = db.session.execute(query).fetchone()
    if exists_user is None:
        return False
    return True

def is_user_a_caretaker(current_user):
    query = "SELECT * FROM CareTakers WHERE username = '{}'".format(current_user.username)
    exists_user = db.session.execute(query).fetchone()
    if exists_user is None:
        return False
    return True

# If false, user is a full Time
# If true, user is a part time
def is_user_a_parttime_caretaker(current_user):
    query = "SELECT * FROM PartTime WHERE username = '{}'".format(current_user.username)
    exists_user = db.session.execute(query).fetchone()
    if exists_user is None:
        return False
    return True

@view.route("/")
@view.route("/home")
def home():
    return render_template('home.html')

@view.route("/about")
def about():
    return render_template('about.html')

@view.route("/caretakers")
def caretakers():
    return render_template('available-caretakers.html')

# Page to bid for a caretaker
@view.route("/bid")
def bid():
    return render_template('bid.html')


# Will be inserted into the caretaker table
@view.route("/registration", methods=["GET", "POST"])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        area = form.area.data
        gender = form.gender.data
        select1 = form.select1.data ## Indicate what he want to sign up as
        select2 = form.select2.data ## Indicate what he want to be ig he sign up as a care taker.
        ## do something to get if he is a pet owner or care taker
        query = "SELECT * FROM users WHERE username = '{}'".format(username)
        exists_user = db.session.execute(query).fetchone()
        if exists_user:
            form.username.errors.append("{} is already in use.".format(username))
        else:
            query = "INSERT INTO users(username, email, area, gender, password) VALUES ('{}', '{}', '{}', '{}', '{}')"\
                .format(username, email, area, gender, password)
            db.session.execute(query)
            query1 = "INSERT INTO PetOwners(username) VALUES ('{}')".format(username)
            query2 = "INSERT INTO CareTakers(username) VALUES ('{}')".format(username)
            if (select1 == '1'):
                db.session.execute(query1)
            elif (select1 == '2'):
                db.session.execute(query2)
            else:
                db.session.execute(query1)
                db.session.execute(query2)
            if (select1 != '1'):
                query3 = "INSERT INTO PartTime(username) VALUES ('{}')".format(username)
                query4 = "INSERT INTO FullTime(username) VALUES ('{}')".format(username)
                if (select2 == '1'):
                    db.session.execute(query3)
                elif (select2 == '2'):
                    db.session.execute(query4)

            ##db.session.execute(query)
            ##db.session.execute(query2)
            db.session.commit()
            ##return "You have successfully signed up as a caretaker!"
            flash("You have successfully signed up!", 'success')
            return redirect(url_for('view.home'))
    return render_template("registration.html", form=form)

@view.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))
    form = LoginForm()
    if form.is_submitted():
        print("username entered:", form.username.data)
        print("password entered:", form.password.data)
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        correct_password = form.password.data == user.password
        ##user = "SELECT * FROM users WHERE username = '{}'".format(form.username.data)
        if user is None:
            flash('Username does not exist, please register for an account first if you have yet to done so.', 'Danger')
        if user and correct_password:
            # TODO: You may want to verify if password is correct
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash("You have successfully logged in!", 'success')
            return redirect(next_page) if next_page else redirect(url_for('view.home'))
            ##return redirect("/privileged-page")
            ##flash("You have successfully logged in!", 'success')
            #return redirect(url_for('view.home'))
        else:
            flash('Wrong username or password!', 'Danger')
    return render_template("login.html", form=form)

@view.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('view.home'))

@view.route("/account", methods=["GET", "POST"])
@login_required # means this route can only use when login
def account():
    return render_template("account.html")

## Need a way to find out
@view.route("/registerpet", methods=["GET", "POST"])
@login_required
def registerpet():
    form = PetRegistrationForm()
    #TO CHECK IF HE IS A PET OWNER OR NOT
    #IF HE IS NOT, WILL BE REDIRECTED TO HOME PAGE
    if is_user_a_petowner(current_user) == False:
        flash("You are not a pet owner, sign up as one first!", 'error')
        return redirect(url_for('view.home'))

    if form.validate_on_submit():
        owner = current_user.username
        pet_name = form.pet_name.data
        check_if_pet_exist = "SELECT * FROM OwnedPets WHERE pet_name = '{}' AND owner = '{}'".format(pet_name, owner)
        exist_pet = db.session.execute(check_if_pet_exist).fetchone()
        if exist_pet:
            flash('You already have a pet with the same name!', 'Danger')
            return redirect(url_for('view.registerpet'))
        category = form.category.data
        age = form.age.data
        special_care1 = form.special_care1.data
        special_care2 = form.special_care2.data
        special_care3 = form.special_care3.data
        query1 = "INSERT INTO OwnedPets(owner, pet_name, category, age) VALUES('{}', '{}', '{}','{}')"\
            .format(owner, pet_name, category, age)
        db.session.execute(query1)
        if special_care1 != "":
            special1 = "SELECT care FROM SpecialCare WHERE care = '{}'".format(special_care1)
            special11 = db.session.execute(special1).fetchone()
            if not special11:
                query2 = "INSERT INTO SpecialCare(care) VALUES('{}')"\
                    .format(special_care1)
                db.session.execute(query2)
            query3 = "INSERT INTO RequireSpecialCare(owner, pet_name, care) VALUES('{}', '{}', '{}')"\
                .format(owner, pet_name, special_care1)
            db.session.execute(query3)
        db.session.commit()
        if special_care2 != "":
            special2 = "SELECT care FROM SpecialCare WHERE care = '{}'".format(special_care2)
            special22 = db.session.execute(special2).fetchone()
            if not special22:
                query2 = "INSERT INTO SpecialCare(care) VALUES('{}')"\
                    .format(special_care2)
                db.session.execute(query2)
            query3 = "INSERT INTO RequireSpecialCare(owner, pet_name, care) VALUES('{}', '{}', '{}')"\
                .format(owner, pet_name, special_care2)
            db.session.execute(query3)
        db.session.commit()
        if special_care3 != "":
            special3 = "SELECT care FROM SpecialCare WHERE care = '{}'".format(special_care3)
            special33 = db.session.execute(special3).fetchone()
            if not special33:
                query2 = "INSERT INTO SpecialCare(care) VALUES('{}')"\
                    .format(special_care3)
                db.session.execute(query2)
            query3 = "INSERT INTO RequireSpecialCare(owner, pet_name, care) VALUES('{}', '{}', '{}')"\
                .format(owner, pet_name, special_care3)
            db.session.execute(query3)
        db.session.commit()
        flash("You have successfully register your pet!", 'success')
        return redirect(url_for('view.home'))
    return render_template("register-pet.html", form=form)

## NEED HELP WITH THIS, DK HOW TO DISPLAY A TABLE FROM A QUERY
@view.route("/petlist", methods=["POST", "GET"])
@login_required
def petlist():
    #petlist = []
    owner = current_user.username
    if is_user_a_petowner(current_user) == False:
        flash("You are not a pet owner, sign up as one first!", 'error')
        return redirect(url_for('view.home'))

    query = "SELECT pet_name, category, age FROM OwnedPets WHERE owner = '{}'".format(owner)
    result = db.session.execute(query)

    result = [r for r in result]
    table = petList(result)
    table.border = True
    return render_template("petlist.html", table=table)
    #return redirect(url_for('view.home'))

##@view.route("/privileged-page", methods=["GET"])
##@login_required
##def render_privileged_page():
##    return "<h1>Hello, {}!</h1>".format(current_user.username)
