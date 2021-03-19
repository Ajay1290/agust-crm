from flask_wtf import FlaskForm
from flask import request

from wtforms import HiddenField, StringField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional, Regexp, EqualTo, ValidationError
from wtforms_components import EmailField, Email
from wtforms_alchemy.validators import Unique

from manager.models import Machine, Employee

from manager.ext import db, dbt
from manager.libs.utils.util_wtforms import ModelForm

class NewComplaintForm(FlaskForm):
    # Genral Info
    nature = StringField('Nature Of Problem',validators=[DataRequired()])
    description = TextAreaField('Description')
    contact_name = StringField('Contact Name')
    contact_phone = StringField('Contact Phone')
    source = StringField('Source')