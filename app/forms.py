from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, IntegerField
from wtforms.validators import InputRequired, Length


class SignupForm(FlaskForm):
    name = StringField('Name', validators=[
        InputRequired(message='Please enter a name.'),
        Length(max=30, message='Too long (max 30 characters).')])
    username = StringField('Username', validators=[
        InputRequired(message='Please enter a username.'),
        Length(max=20, message='Too long (max 20 characters).')])
    passphrase = PasswordField('Passphrase', validators=[
        InputRequired(message='Please enter a passphrase.')])
    pass_verify = PasswordField('Re-enter passphrase', validators=[
        InputRequired(message='Please re-enter your passphrase.')])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(message='Please enter your username.')])
    passphrase = PasswordField('Passphrase', validators=[
        InputRequired(message='Please enter your passphrase.')])


class TradeForm(FlaskForm):
    from_fiats = SelectField('Origin')
    from_cryptos = SelectField('Origin')
    from_comms = SelectField('Origin')
    to_fiats = SelectField('Destination')
    to_cryptos = SelectField('Destination')
    to_comms = SelectField('Destination')
    amount = IntegerField('Amount sold', validators=[InputRequired()])
    date = DateField('Date', validators=[InputRequired()])
