from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, EqualTo
from wtforms_components import EmailField, Email
from wtforms_alchemy.validators import Unique

from manager.ext import db
from manager.models.users import User
from manager.libs.utils.util_wtforms import ModelForm
from manager.libs.validations import ensure_identity_exists, ensure_existing_password_matches


class LoginForm(FlaskForm):
    next = HiddenField()
    identity = StringField('Username or email', validators=[DataRequired(), Length(3, 254)])
    password = PasswordField('Password',  validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('Stay signed in')


class BeginPasswordResetForm(FlaskForm):
    identity = StringField('Username or email', validators=[DataRequired(), Length(3, 254), ensure_identity_exists])


class PasswordResetForm(FlaskForm):
    reset_token = HiddenField()
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])


class SignupForm(ModelForm):
    username = StringField(validators=[DataRequired(), Unique(User.username, get_session=lambda: db.session)])
    email = EmailField(validators=[DataRequired(), Email(), Unique(User.email, get_session=lambda: db.session)])
    password = PasswordField(validators=[DataRequired(), Length(8, 128)])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])


class SendEmailAgainForm(ModelForm):
    send = SubmitField('Send Again')


class UpdateCredentials(ModelForm):
    current_password = PasswordField('Current password', [DataRequired(), Length(8, 128), ensure_existing_password_matches])
    email = EmailField(validators=[Email(), Unique(User.email, get_session=lambda: db.session)])
    password = PasswordField('Password', [Optional(), Length(8, 128)])
