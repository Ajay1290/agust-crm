from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, AnyOf
    

class CreditCardForm(FlaskForm):
    address = TextAreaField('Address', [DataRequired(), Length(6, 254)])
    phone = StringField('Phone', [DataRequired(), Length(6, 13)])
    pincode = StringField('Pincode', [DataRequired(), Length(1, 254)])
    stripe_key = HiddenField('Stripe publishable key', [DataRequired(), Length(1, 254)])
    plan = HiddenField('Plan', [DataRequired(), Length(1, 254)])
    coupon_code = StringField('Do you have a coupon code?', [Optional(), Length(1, 128)])
    name = StringField('Name on card', [DataRequired(), Length(1, 254)])
    cvc = StringField('CVC', [DataRequired(), Length(3,3, message="3 digit long required")])


class UpdateSubscriptionForm(FlaskForm):
    coupon_code = StringField('Do you have a coupon code?', [Optional(), Length(1, 254)])


class CancelSubscriptionForm(FlaskForm):
    pass
