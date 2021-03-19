from flask_wtf import Form
from flask import request

from wtforms import HiddenField, StringField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional, Regexp, EqualTo, ValidationError
from wtforms_components import EmailField, Email
from wtforms_alchemy.validators import Unique


from manager.models import Customer
from manager.ext import db, dbt
from manager.libs.validations import ensure_identity_exists, ensure_existing_password_matches
from manager.libs.utils.util_wtforms import ModelForm

def edit_lvl_gst_uniquness(form, field):    
    cus_id = request.path.lstrip('/sales/customer/').rstrip('/edit')
    cus = dbt.session.query(Customer).get_or_404(cus_id)
    if field.data != cus.gst:
        if Customer.query.filter(Customer.gst == field.data).first():
            raise ValidationError(f'Enter Unique GST No.')


class NewCustomerForm(ModelForm):
    # Genral Info
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name')
    company = StringField('Company')
    display_name = StringField('Display Name',validators=[DataRequired(),
                                                Unique(Customer.display_name, get_session=lambda: db.session)])
    customer_type = SelectField(u'Customer Type',
                            choices=[('Consumer', 'Consumer'), ('GST Registered', 'GST Registered'), ('GST Unregistered', 'GST Unregistered')])

    # Contant Info
    phone = StringField('Phone', validators=[Optional() ,Length(6, 13)])
    email = EmailField('Email', validators=[Optional(), Email()])
    website = StringField('Website')

    # Billing Address
    address = TextAreaField('Billing Address')
    pincode = StringField('Billing Pincode')
    city = StringField('Billing City')
    state = StringField('Billing State')
    country = StringField('Billing Country')

    # Shiping Address
    s_address = TextAreaField('Shipping Address')
    s_pincode = StringField('Shipping Pincode')
    s_city = StringField('Shipping City')
    s_state = StringField('Shipping State')
    s_country = StringField('Shipping Country')


    # Tax Info
    gst = StringField('GST No.', validators=[Optional(), Unique(Customer.gst, get_session=lambda: db.session), 
                                            Regexp(r'\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}')])
    pan = StringField('PAN No.', validators=[Optional(), Unique(Customer.pan, get_session=lambda: db.session),
                                            Regexp(r'^[a-zA-Z]{5}[0-9]{4}[a-zA-Z]$')])

class EditCustomerForm(ModelForm):    
    # Genral Info
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name')
    company = StringField('Company')
    display_name = StringField('Display Name',validators=[DataRequired()])
    customer_type = SelectField(u'Customer Type',
                            choices=[('Consumer', 'Consumer'), ('GST Registered', 'GST Registered'), ('GST Unregistered', 'GST Unregistered')])

    # Contant Info
    phone = StringField('Phone', validators=[Optional() ,Length(6, 13)])
    email = EmailField('Email', validators=[Optional(), Email()])
    website = StringField('Website')

    # Billing Address
    address = TextAreaField('Billing Address')
    pincode = StringField('Billing Pincode')
    city = StringField('Billing City')
    state = StringField('Billing State')
    country = StringField('Billing Country')

    # Shiping Address
    s_address = TextAreaField('Shipping Address')
    s_pincode = StringField('Shipping Pincode')
    s_city = StringField('Shipping City')
    s_state = StringField('Shipping State')
    s_country = StringField('Shipping Country')


    # Tax Info
    gst = StringField('GST No.', validators=[Optional(), edit_lvl_gst_uniquness, Regexp(r'\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}')])
    pan = StringField('PAN No.', validators=[Optional(), Unique(Customer.pan, get_session=lambda: db.session), Regexp(r'^[a-zA-Z]{5}[0-9]{4}[a-zA-Z]$')])    

class NewContactForm(ModelForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[Optional() ,Length(6, 13)])
    email = StringField('Email', validators=[Optional()])
    website = StringField('Website', validators=[Optional()])

class EditContactForm(ModelForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[Optional() ,Length(6, 13)])
    email = StringField('Email', validators=[Optional()])
    website = StringField('Website', validators=[Optional()])