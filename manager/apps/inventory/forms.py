from flask_wtf import Form
from flask import request
from wtforms import HiddenField, StringField, PasswordField, BooleanField, TextAreaField, SelectField, DateField
from wtforms.fields import IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, Optional, Regexp, EqualTo, ValidationError
from wtforms_components import EmailField, Email
from wtforms_alchemy.validators import Unique
from manager.libs.utils.util_wtforms import ModelForm
from manager.models import Machine, Consumable, Service
from manager.ext import db, dbt
from manager.libs.validations import ensure_identity_exists, ensure_existing_password_matches

# Machines Form -----------------------------------------------------
class NewMachineForm(ModelForm):
    # Genral Info
    name = StringField('Name', validators=[DataRequired(), 
                                    Unique(Machine.name, get_session=lambda: dbt.session)])
    product_code = StringField('Product Code')
    category = StringField('Category')
    description = TextAreaField('Description')

    model = StringField('Model')
    serial = StringField('Serial No.')
    instdate = DateField('Installation Date')

# Consumable Form -----------------------------------------------------
class NewConsumableForm(ModelForm):
    name = StringField('Name', validators=[DataRequired(), 
                                    Unique(Consumable.name, get_session=lambda: dbt.session)])
    product_code = StringField('Product Code')
    category = StringField('Category')
    description = TextAreaField('Description')
    model = StringField('Model')
    unit =  SelectField(u'Unit',
                            choices=[   ('BAG', 'BAG - BAGS'),
                                        ('BOT', 'BOT - BOTTLES'),
                                        ('BOX', 'BOX - BOXES'),
                                        ('CMS', 'CMS - CENTIMETERS'),                                        
                                        ('CAN', 'CAN - CANS'),
                                        ('DOZ', 'DOZ - DOZENS'),
                                        ('DRUM', 'DRUM - DRUMS'),                                        
                                        ('KGS', 'KGS - KILLOGRAMS'),
                                        ('PCS', 'PCS - PIECES'),
                                        ('PAC', 'PAC - PACKS'),
                                        ('TON', 'TON - TONES'),
                                        ('UNT', 'UNT - UNITS'),                                        
                                        ('YDS', 'YDS - YARDS'),                                        
                                    ]
                        )
    qty = IntegerField("Qty", validators=[Optional()])
    sales_price = DecimalField("Sales Price", validators=[Optional()], places=2)
    low_stock_alert = IntegerField('Low Stock Alert', validators=[Optional()])

# Assign Customer Form ---------------------------------------------------
class AssignCustomerForm(ModelForm):
    pass