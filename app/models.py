from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model, UserMixin):
    '''User Model
    ```sql
    id SERIAL PK,
    name VARCHAR(30) NOT NULL,
    username VARCHAR(20) NOT NULL UNIQUE,
    pass_hash TEXT NOT NULL
    ```'''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    pass_hash = db.Column(db.Text, nullable=False)

    fiats = db.relationship(
        'Fiat_curr', secondary='saved_fiats', backref='users')
    cryptos = db.relationship(
        'Crypto_curr', secondary='saved_cryptos', backref='users')
    comms = db.relationship(
        'Commodity', secondary='saved_comms', backref='users')
    trades = db.relationship('Trade', backref='user')

    def __repr__(self) -> str:
        return f'<User {self.id}: {self.username}>'

    @classmethod
    def signup(cls, name, username, pwd):
        '''Hashes pass and returns new user instance'''
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode('utf8')

        return cls(name=name, username=username, pass_hash=hashed_utf8)

    @classmethod
    def login(cls, username, pwd):
        '''Returns user if valid username and passphrase, else false'''
        u = cls.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.pass_hash, pwd):
            return u
        else:
            return False


class Fiat_curr(db.Model):
    '''Fiat Currency Model
    ```sql
    symbol VARCHAR(8) PK,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    icon VARCHAR(5) NOT NULL (eg $)
    ```'''
    __tablename__ = 'fiat_currencies'

    symbol = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(5), nullable=False)

    def __repr__(self) -> str:
        return f'<Fiat_curr {self.symbol}: {self.name}>'


class Crypto_curr(db.Model):
    '''Cryptocurrency Model
    ```sql
    symbol VARCHAR(8) PK,
    name TEXT NOT NULL
    ```'''
    __tablename__ = 'crypto_currencies'

    symbol = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return f'<Crypto_curr {self.symbol}: {self.name}>'


class Commodity(db.Model):
    '''Commodities Model
    ```sql
    symbol VARCHAR(8) PK,
    name TEXT NOT NULL,
    descr TEXT,
    query_link TEXT NOT NULL,
    col TEXT NOT NULL
    ```'''
    __tablename__ = 'commodities'

    symbol = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.Text, nullable=False)
    descr = db.Column(db.Text)
    query_link = db.Column(db.Text, nullable=False)
    col = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return f'<Commodity {self.symbol}: {self.name}>'


class Saved_Fiat(db.Model):
    '''User to Fiat Curr relationship table
    ```sql
    id SERIAL PK,
    user_id INT NOT NULL REFS users
    symbol VARCHAR(8) NOT NULL REFS fiat_currencies
    ```'''
    __tablename__ = 'saved_fiats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'), nullable=False)
    symbol = db.Column(db.String(8), db.ForeignKey(
        'fiat_currencies.symbol', ondelete='cascade'), nullable=False)


class Saved_Crypto(db.Model):
    '''User to Crypto Curr relationship table
    ```sql
    id SERIAL PK,
    user_id INT NOT NULL REFS users
    symbol VARCHAR(8) NOT NULL REFS crypto_currencies
    ```'''
    __tablename__ = 'saved_cryptos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'), nullable=False)
    symbol = db.Column(db.String(8), db.ForeignKey(
        'crypto_currencies.symbol', ondelete='cascade'), nullable=False)


class Saved_Comm(db.Model):
    '''User to Commodity relationship table
    ```sql
    id SERIAL PK,
    user_id INT NOT NULL REFS users
    symbol VARCHAR(8) NOT NULL REFS commodities
    ```'''
    __tablename__ = 'saved_comms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'), nullable=False)
    symbol = db.Column(db.String(8), db.ForeignKey(
        'commodities.symbol', ondelete='cascade'), nullable=False)


class Trade(db.Model):
    '''User's Trade Model
    ```sql
    id SERIAL PK,
    user_id INT NOT NULL REFS users.id,
    date_traded TIMESTAMP NOT NULL,
    from_symbol TEXT NOT NULL,
    from_amount FLOAT NOT NULL,
    to_symbol TEXT NOT NULL,
    to_amount FLOAT NOT NULL,
    btc_equiv_then FLOAT NOT NULL
    ```'''
    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'), nullable=False)

    date_traded = db.Column(db.DateTime, nullable=False)
    from_symbol = db.Column(db.Text, nullable=False)
    from_amount = db.Column(db.Float, nullable=False)
    to_symbol = db.Column(db.Text, nullable=False)
    to_amount = db.Column(db.Float, nullable=False)
    btc_equiv_then = db.Column(db.Float, nullable=False)

    def get_historical_trades(self):
        '''Returns to_amount and btc_equiv_then from added trade'''
        from helpers import get_prices
        (self.to_amount, self.btc_equiv_then) = get_prices()
