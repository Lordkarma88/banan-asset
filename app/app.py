from flask import Flask, request, render_template, redirect
from flask import flash, url_for, jsonify, abort
from flask_login import LoginManager, login_user, logout_user
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from os import environ
from datetime import date

from models import db, connect_db, User, Fiat_curr, Crypto_curr, Commodity
from forms import SignupForm, LoginForm, TradeForm
from helpers import update_crypto_data, get_btc_price, get_prices, format_price
# from secret_keys import flask_secret_key

GET = 'GET'
POST = 'POST'

app = Flask(__name__)
# for secret keys and env vars that change depending on env
# .env is ignored by git and has all secret keys
# other env (railway) has its own env vars
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get('FLASK_SECRET_KEY')

BASE_URL = environ.get('BASE_URL')

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
    '''Show landing page with form for trying app out'''
    form = TradeForm()

    add_choices(form)
    today = date.today().strftime('%Y-%m-%d')

    return render_template('index.html', form=form, today=today)


def add_choices(form, user=False):
    '''Makes list of tuples of assets and add the choices to the form
        If user=True, only add the user's selected assets'''

    fiat_query = db.session.query(
        Fiat_curr.symbol, Fiat_curr.country).order_by(Fiat_curr.symbol)
    crypto_query = db.session.query(
        Crypto_curr.symbol, Crypto_curr.name).order_by(Crypto_curr.symbol)
    comm_query = db.session.query(
        Commodity.symbol, Commodity.name).order_by(Commodity.name)

    if user:  # Only select user's assets if not the home page
        fiat_query = fiat_query.filter(
            Fiat_curr.users.contains(current_user))
        crypto_query = crypto_query.filter(
            Crypto_curr.users.contains(current_user))
        comm_query = comm_query.filter(
            Commodity.users.contains(current_user))

    fiat_choices = [(ch[0], f'{ch[0]} ({ch[1]})') for ch in fiat_query.all()]
    crypto_choices = [(ch[0], f'{ch[0]} ({ch[1]})')
                      for ch in crypto_query.all()]
    comm_choices = [tuple(ch) for ch in comm_query.all()]

    # fiat_choices.insert(0, ('', 'Select a fiat currency...'))
    # crypto_choices.insert(0, ('', 'Select a cryptocurrency...'))
    # comm_choices.insert(0, ('', 'Select a commodity...'))

    form.from_fiats.choices = form.to_fiats.choices = fiat_choices
    form.from_cryptos.choices = form.to_cryptos.choices = crypto_choices
    form.from_comms.choices = form.to_comms.choices = comm_choices

    return


@app.route('/mytrades')
def my_trades():
    '''Show logged in landing page'''
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    trades = current_user.trades

    form = TradeForm()
    add_choices(form, user=True)

    return render_template('user/my_trades.html', trades=trades, form=form)


########################
#     API METHODS      #
########################

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
        return redirect(url_for('my_trades'))

    form = SignupForm()

    if form.validate_on_submit():
        u = register_user(form)

        if u:
            login_user(u)
            flash('signed up', 'success')
            return redirect(url_for('my_trades'))

    validity = {}
    for field in form:
        validity[field.id] = ''
        if field.errors:
            validity[field.id] = 'invalid'

    return render_template('auth/signup.html', form=form, validity=validity)


def register_user(form):
    '''Accepts validated form and adds user to DB.\n
    Returns False if passphrases don't match
    or if username taken (IntegrityError).'''
    name = form.name.data
    username = form.username.data
    passphrase = form.passphrase.data
    pass_verify = form.pass_verify.data

    if passphrase != pass_verify:
        form.pass_verify.errors = ["Passphrases don't match."]
        return False

    u = User.signup(name, username, passphrase)
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
        return redirect(url_for('my_trades'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        passphrase = form.passphrase.data
        u = User.login(username, passphrase)

        if u:
            login_user(u)
            flash('welcome back', 'success')
            return redirect(url_for('my_trades'))

        form.username.errors = ['Invalid username or passphrase.']

    validity = {}
    for field in form:
        validity[field.id] = ''
        if field.errors:
            validity[field.id] = 'invalid'

    return render_template('auth/login.html', form=form, validity=validity)


@app.route('/logout')
def logout():
    '''Log out user if logged in'''
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    logout_user()
    return redirect(url_for('home'))
