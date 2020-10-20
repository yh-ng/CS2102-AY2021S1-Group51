from flask import Blueprint, redirect, render_template, flash, url_for, request
from flask_login import current_user, login_required, login_user, UserMixin, logout_user

from __init__ import db, login_manager
from forms import LoginForm, RegistrationForm
from models import Users

view = Blueprint("view", __name__)


@login_manager.user_loader
def load_user(username):
    user = Users.query.filter_by(username=username).first()
    return user or current_user


#@view.route("/", methods=["GET"])
#def render_dummy_page():
#    return "<h1>CS2102</h1>\
#    <h2>Flask App started successfully!</h2>"

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
@view.route("/register_caretaker", methods=["GET", "POST"])
def register_caretaker():
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        ## do something to get if he is a pet owner or care taker
        query = "SELECT * FROM users WHERE username = '{}'".format(username)
        exists_user = db.session.execute(query).fetchone()
        if exists_user:
            form.username.errors.append("{} is already in use.".format(username))
        else:
            query = "INSERT INTO users(username, email, password) VALUES ('{}', '{}', '{}')"\
                .format(username, email, password)
            query2 = "INSERT INTO CareTakers(username) VALUES ('{}')"\
                .format(username)
            db.session.execute(query)
            db.session.execute(query2)
            db.session.commit()
            ##return "You have successfully signed up as a caretaker!"
            flash("You have successfully signed up as a caretaker!", 'success')
            return redirect(url_for('home'))
    return render_template("registration-caretaker.html", form=form)

## Will be inserted into the pet owner table as well
@view.route("/register_petowner", methods=["GET", "POST"])
def register_petowner():
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        ## do something to get if he is a pet owner or care taker
        query = "SELECT * FROM users WHERE username = '{}'".format(username)
        exists_user = db.session.execute(query).fetchone()
        if exists_user:
            form.username.errors.append("{} is already in use.".format(username))
        else:
            query = "INSERT INTO users(username, email, password) VALUES ('{}', '{}', '{}')"\
                .format(username, email, password)
            query2 = "INSERT INTO PetOwners(username) VALUES ('{}')"\
                .format(username)
            db.session.execute(query)
            db.session.execute(query2)
            db.session.commit()
            flash("You have successfully signed up as a petowner!", 'success')
            return redirect(url_for('home'))
    return render_template("registration_petowner.html", form=form)

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

##@view.route("/privileged-page", methods=["GET"])
##@login_required
##def render_privileged_page():
##    return "<h1>Hello, {}!</h1>".format(current_user.username)
