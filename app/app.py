from flask import Flask, request, render_template, redirect
from flask import flash, url_for, jsonify, abort
from flask_login import LoginManager, login_user, logout_user
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from datetime import date

from models import db, connect_db, User, Fiat_curr, Crypto_curr, Commodity
from forms import SignupForm, LoginForm, TradeForm
from helpers import update_crypto_data, get_btc_price, get_prices, format_price
from secret_keys import flask_secret_key

GET = 'GET'
POST = 'POST'
BASE_URL = 'http://127.0.0.1:5000'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bbanan-asset'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = flask_secret_key


# def init_app():
#     connect_db(app)
#     update_crypto_data()


# init_app()

connect_db(app)

login_manager = LoginManager()
login_manager.init_app(app)

update_crypto_data()


@app.errorhandler(404)
def not_found(e):
    '''Show error page'''
    return render_template('404.html')


@app.template_global()
def formatted_btc_price(at_date=None):
    if not at_date:
        at_date = date.today().strftime('%Y-%m-%d')
    return format_price(get_btc_price(at_date))


@app.route('/')
def home():
    form = TradeForm()

    choices = get_choices()
    form.from_fiats.choices, form.from_cryptos.choices, form.from_comms.choices = choices
    form.to_fiats.choices, form.to_cryptos.choices, form.to_comms.choices = choices

    today = date.today().strftime('%Y-%m-%d')

    return render_template('index.html', form=form, today=today)


def get_choices():
    '''Return list of tuples to be passed to WTForms SelectField choices'''
    fiat_tuples = db.session.query(
        Fiat_curr.symbol, Fiat_curr.country).order_by(
        Fiat_curr.symbol).all()
    fiat_choices = [(ch[0], f'{ch[0]} ({ch[1]})') for ch in fiat_tuples]
    # fiat_choices.insert(0, ('', 'Select a fiat currency...'))

    crypto_tuples = db.session.query(
        Crypto_curr.symbol, Crypto_curr.name).order_by(
        Crypto_curr.symbol).all()
    crypto_choices = [(ch[0], f'{ch[0]} ({ch[1]})') for ch in crypto_tuples]
    # crypto_choices.insert(0, ('', 'Select a cryptocurrency...'))

    comm_tuples = db.session.query(
        Commodity.symbol, Commodity.name).order_by(
        Commodity.name).all()
    comm_choices = [tuple(ch) for ch in comm_tuples]
    # comm_choices.insert(0, ('', 'Select a commodity...'))
    return (fiat_choices, crypto_choices, comm_choices)


@app.route('/convert', methods=[POST])
def convert():
    '''Returns converted values from APIs. Adds trade to user if logged in.'''
    # Prevent outside requests from spamming the server
    if request.environ.get('HTTP_ORIGIN') != BASE_URL:
        return abort(403)

    from_sym = request.json['from_sym']
    to_sym = request.json['to_sym']
    amount = request.json['amount']
    date = request.json['date']

    tsym_equiv, btc_equiv, btc_price = get_prices(
        from_sym, to_sym, float(amount), date)

    if not tsym_equiv:
        return jsonify({'error': btc_equiv})

    return jsonify({'tsym_equiv': tsym_equiv,
                    'btc_equiv': btc_equiv,
                    'btc_price': btc_price})

########################
#    AUTHENTICATION    #
########################


@login_manager.user_loader
def load_user(user_id):
    '''Required by flask-login'''
    return User.query.get(user_id)


@app.route('/signup', methods=[GET, POST])
def sign_up():
    '''Show signup form and add user to DB when submitted'''
    if current_user.is_authenticated:
        flash('already logged in', 'danger')
        return redirect(url_for('home'))

    form = SignupForm()

    if form.validate_on_submit():
        u = register_user(form)

        if u:
            login_user(u)
            flash('signed up', 'success')
            return redirect(url_for('home'))

    validity = {}
    for field in form:
        validity[field.id] = ''
        if field.errors:
            validity[field.id] = 'invalid'

    return render_template('/auth/signup.html', form=form, validity=validity)


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
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        u = User.login(username, password)

        if u:
            login_user(u)
            flash('logged in', 'success')
            return redirect(url_for('home'))

        form.username.errors = ['Invalid username or password.']
    return render_template('auth/login.html', form=form)


@app.route('/logout')
def logout():
    '''Log out user if logged in'''
    if current_user.is_anonymous:
        flash("You aren't logged in!", 'danger')
        return redirect(url_for('login'))

    logout_user()
    flash('logged out', 'warning')
    return redirect(url_for('home'))
