from flask import Flask, request, render_template, redirect, flash
from flask_login import LoginManager, login_user, logout_user
from flask_login import login_required, current_user
import requests
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Fiat_curr, Crypto_curr, Commodity
from forms import SignupForm, LoginForm

from secret_keys import flask_secret_key, Nasdaq_key, CCompare_key
GET = 'GET'
POST = 'POST'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bbanan-asset'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = flask_secret_key

connect_db(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup', methods=[GET, POST])
def sign_up():
    if current_user.is_authenticated:
        flash('already logged in', 'danger')
        return redirect('/')

    form = SignupForm()

    if form.validate_on_submit():
        u = register_user(form)

        if u:
            login_user(u)
            flash('signed up', 'success')
            return redirect('/')

    return render_template('/auth/signup.html', form=form)


def register_user(form):
    '''Accepts validated form and adds user to DB.\n
    Returns False if passwords don't match
    or if username taken (IntegrityError).'''
    name = form.name.data
    username = form.username.data
    password = form.password.data
    pass_verify = form.pass_verify.data

    if password != pass_verify:
        form.pass_verify.errors = ["Passwords don't match."]
        return False

    u = User.signup(name, username, password)
    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        form.username.errors = ['This username is already taken.']
        return False
    return u


@app.route('/login', methods=[GET, POST])
def login():
    '''Login user or show login form'''
    if current_user.is_authenticated:
        flash('already logged in', 'danger')
        return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        u = User.login(username, password)

        if u:
            login_user(u)
            flash('logged in', 'success')
            return redirect('/')

        form.username.errors = ['Invalid username or password.']
    return render_template('auth/login.html', form=form)


@app.route('/logout')
def logout():
    # import pdb
    # pdb.set_trace()
    if current_user.is_anonymous:
        flash('not logged in', 'danger')
        return redirect('/')
    logout_user()
    flash('logged out', 'warning')
    return redirect('/')
