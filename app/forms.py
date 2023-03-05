from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, FloatField
from wtforms.validators import InputRequired, Length


class SignupForm(FlaskForm):
    name = StringField('Name', validators=[
        InputRequired(message='Please enter a name.'),
        Length(max=30, message='Too long (max 30 characters).')])
    username = StringField('Username', validators=[
        InputRequired(message='Please enter a username.'),
        Length(max=20, message='Too long (max 20 characters).')])
    password = PasswordField('Password', validators=[
        InputRequired(message='Please enter a password.')])
    pass_verify = PasswordField('Re-enter password', validators=[
        InputRequired(message='Please re-enter your password.')])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(message='Please enter your username.')])
    password = PasswordField('Password', validators=[
        InputRequired(message='Please enter your password.')])


class TradeForm(FlaskForm):
    from_fiats = SelectField('Fiat currencies')
    from_cryptos = SelectField('Crypto currencies')
    from_comms = SelectField('Commodities')
    to_fiats = SelectField('Fiat currencies')
    to_cryptos = SelectField('Crypto currencies')
    to_comms = SelectField('Commodities')
    amount = FloatField('Amount', validators=[InputRequired()])
    date = DateField('Date', validators=[InputRequired()])
