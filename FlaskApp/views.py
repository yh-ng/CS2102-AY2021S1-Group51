from flask import Blueprint, redirect, render_template, flash, url_for, request
from flask_login import current_user, login_required, login_user, UserMixin, logout_user

from __init__ import db, login_manager
from forms import LoginForm, RegistrationForm, PetRegistrationForm
from models import Users

view = Blueprint("view", __name__)


@login_manager.user_loader
def load_user(username):
    user = Users.query.filter_by(username=username).first()
    return user or current_user

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
        select1 = form.select1.data ## Indicate what he want to sign up as
        select2 = form.select2.data ## Indicate what he want to be ig he sign up as a care taker.
        ## do something to get if he is a pet owner or care taker
        query = "SELECT * FROM users WHERE username = '{}'".format(username)
        exists_user = db.session.execute(query).fetchone()
        if exists_user:
            form.username.errors.append("{} is already in use.".format(username))
        else:
            query = "INSERT INTO users(username, email, area, password) VALUES ('{}', '{}', '{}', '{}')"\
                .format(username, email, area, password)
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
            flash('Wrong username or password!')
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
        owner_name = current_user.username

        pet_name = form.pet_name.data
        category = form.category.data
        age = form.age.data
        special_care = form.special_care.data
        if special_care == "":
            query1 = "INSERT INTO OwnedPets(owner_name, pet_name, category, age) VALUES('{}', '{}', '{}', '{}')"\
                .format(owner_name, pet_name, category, age)
            db.session.execute(query1)
            flash("You have successfully register your pet!", 'success')
        else:
            ## Query to insert into Special Care table first
            ##query2 = "INSERT INTO"
            # Query to insert into OwnedPets Table
            query3 = "INSERT INTO OwnedPets(owner_name, pet_name, category, age) VALUES('{}', '{}', '{}', '{}')"\
                .format(owner_name, pet_name, category, age)
            ## Query to insert into RequireSpecialCare Table
            db.session.execute(query3)
        db.session.commit()
        return redirect(url_for('view.home'))
    return render_template("register-pet.html", form=form)




##@view.route("/privileged-page", methods=["GET"])
##@login_required
##def render_privileged_page():
##    return "<h1>Hello, {}!</h1>".format(current_user.username)
