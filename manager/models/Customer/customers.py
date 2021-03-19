from manager.ext import db,dbt
from manager.libs.utils.util_sqlalchemy import ResourceMixin

class Customer(ResourceMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # Genral Info
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(65))
    
    display_name = db.Column(db.String(145), nullable=False)
    company = db.Column(db.String(125))
    customer_type = db.Column(db.String(45))

    # Contant Info
    phone = db.Column(db.String(15), server_default='')
    email = db.Column(db.String(45), server_default='')    
    website = db.Column(db.String(255), server_default='')

    # Billing Address
    address = db.Column(db.String(200), server_default='')
    pincode = db.Column(db.String(25), server_default='')
    city = db.Column(db.String(45), server_default='')
    state = db.Column(db.String(45), server_default='')
    country = db.Column(db.String(45), server_default='')

    # Shiping Address
    s_address = db.Column(db.String(200), server_default='')
    s_pincode = db.Column(db.String(25), server_default='')
    s_city = db.Column(db.String(45), server_default='')
    s_state = db.Column(db.String(45), server_default='')
    s_country = db.Column(db.String(45), server_default='')

    # Tax Info
    gst = db.Column(db.String(15), server_default='')
    pan = db.Column(db.String(10), server_default='')

    # Meta Info
    is_active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # Relationships
    machines = db.relationship('Machine', backref='owner', lazy=True)
    contacts = db.relationship('Contact', backref='in_reach', lazy=True)